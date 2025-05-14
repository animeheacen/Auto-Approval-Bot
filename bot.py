import os import logging from pyrogram import Client, filters, enums from pyrogram.types import ( Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest, CallbackQuery ) from pymongo import MongoClient

Configure logging

logging.basicConfig( level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' ) logger = logging.getLogger(name)

Load environment variables

API_ID = int(os.getenv("API_ID")) API_HASH = os.getenv("API_HASH") BOT_TOKEN = os.getenv("BOT_TOKEN") FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "") SUDO = int(os.getenv("SUDO")) MONGO_URI = os.getenv("MONGO_URI") PHOTO_URL = os.getenv("PHOTO_URL", "https://telegra.ph/file/5f40e53f0f8a6c3a1e8e4.jpg")

Initialize Pyrogram client

app = Client( "auto_approval_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN )

Initialize MongoDB

mongo_client = MongoClient(MONGO_URI) db = mongo_client["auto_approval_bot"] users_col = db["users"]

async def is_user_member(user_id: int): if not FORCE_CHANNEL: return True try: chat_member = await app.get_chat_member(FORCE_CHANNEL, user_id) return chat_member.status not in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED] except Exception as e: logger.error(f"Error checking channel subscription: {e}") return False

@app.on_message(filters.command("start")) async def start_command(client: Client, message: Message): user_id = message.from_user.id user_name = message.from_user.first_name

# Check force subscription
if not await is_user_member(user_id):
    await message.reply_photo(
        photo=PHOTO_URL,
        caption=f"**🍁 ʜᴇʟʟᴏ {user_name}!\n\nʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{FORCE_CHANNEL}")],
            [InlineKeyboardButton("ᴛʀʏ ᴀɢᴀɪɴ", callback_data="check_sub")]
        ])
    )
    return

# Save user to database
users_col.update_one(
    {"user_id": user_id},
    {"$set": {"user_name": user_name}},
    upsert=True
)

# Send welcome message
await message.reply_photo(
    photo=PHOTO_URL,
    caption=f"""**🍁 ʜᴇʟʟᴏ {user_name}!\n\nɪ'ᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ. ɪ ᴄᴀɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴘᴘʀᴏᴠᴇ ᴜsᴇʀs ɪɴ ᴄʜᴀɴɴᴇʟs & ɢʀᴏᴜᴘs. ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴡɪᴛʜ 'ᴀᴅᴅ ᴍᴇᴍʙᴇʀs' ʀɪɢʜᴛs.**""",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴀɴɪᴍᴇ ꜰʟᴀsʜᴇʀ", url="https://t.me/anime_flasher")],
        [InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")],
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{client.me.username}?startchannel=true")]
    ])
)

@app.on_chat_join_request() async def approve_join_request(client: Client, join_request: ChatJoinRequest): try: # Approve the join request await join_request.approve()

# Get chat information
    chat = await client.get_chat(join_request.chat.id)
    
    # Send welcome message to user
    await client.send_photo(
        join_request.from_user.id,
        photo=PHOTO_URL,
        caption=f"""**ʜᴇʟʟᴏ {join_request.from_user.first_name}!\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ!\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chat.title}**\n\n__ᴘᴏᴡᴇʀᴇᴅ ʙʏ: ᴀɴɪᴍᴇ ꜰʟᴀsʜᴇʀ__"""
    )
    
    logger.info(f"Approved join request for {join_request.from_user.id} in {chat.title}")
except Exception as e:
    logger.error(f"Error approving join request: {e}")

@app.on_callback_query(filters.regex("^check_sub$")) async def check_sub_callback(client: Client, callback_query: CallbackQuery): if await is_user_member(callback_query.from_user.id): await callback_query.message.delete() await start_command(client, callback_query.message) else: await callback_query.answer("You haven't joined the channel yet!", show_alert=True)

@app.on_callback_query(filters.regex("^about$")) async def show_about(client: Client, callback_query: CallbackQuery): await callback_query.answer() await callback_query.message.edit_text( text=""" ◈ ᴄʀᴇᴀᴛᴏʀ: ʟᴏᴋɪɪ ᴛᴇɴ ɴᴏ
◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ: ʟᴏᴋɪɪ ᴛᴇɴ ɴᴏ
◈ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ: ᴀɴɪᴍᴇ ғʟᴀsʜᴇʀ
◈ ᴏɴɢᴏɪɴɢ ᴄʜᴀɴɴᴇʟ: ᴏɴɢᴏɪɴɢ ғʟᴀsʜᴇʀ
◈ ʜᴇɴᴛᴀɪ: ʜᴇɴᴛᴀɪ ғʟᴀsʜᴇʀ
◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ: ʜᴜɴᴛᴇʀ """, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_start")] ]) )

@app.on_callback_query(filters.regex("^back_to_start$")) async def back_to_start(client: Client, callback_query: CallbackQuery): await callback_query.message.delete() await start_command(client, callback_query.message)

@app.on_message(filters.command("stats") & filters.user(SUDO)) async def stats_command(client: Client, message: Message): total_users = users_col.count_documents({}) await message.reply_text(f"📊 Bot Stats:\n\nTotal Users: {total_users}")

if name == "main": logger.info("Starting Auto Approval Bot...") app.run()

