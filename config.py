import os

# Telegram API Configuration (required)
API_ID = int(os.getenv("API_ID", 12345678))  # From my.telegram.org
API_HASH = os.getenv("API_HASH", "your_telegram_api_hash_here")  # From my.telegram.org
BOT_TOKEN = os.getenv("BOT_TOKEN", "1234567890:your_bot_token_here")  # From @BotFather

# Channel Configuration (required)
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "your_channel_username")  # Without @
SUDO = int(os.getenv("SUDO", 1234567890))  # Your Telegram user ID

# Database Configuration (required)
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://username:password@cluster0.mongodb.net/yourdbname?retryWrites=true&w=majority"
)

# Media URLs (optional with defaults)
PHOTO_URL = os.getenv(
    "PHOTO_URL",
    "https://telegra.ph/file/5f40e53f0f8a6c3a1e8e4.jpg"  # Default welcome image
)
BACKUP_PHOTO_URL = os.getenv(
    "BACKUP_PHOTO_URL",
    "https://telegra.ph/file/7a3b5d2e8f1d5a9b6c4d2.jpg"  # Default approval image
)

# Advanced Settings (optional)
MAX_APPROVALS_PER_MINUTE = int(os.getenv("MAX_APPROVALS_PER_MINUTE", 30))  # Rate limiting
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "")  # Channel ID for logging (optional)
