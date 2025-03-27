"""
Configuration package for Capybara Sui Bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')

# Discord
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID', '')

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Other APIs
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '') 