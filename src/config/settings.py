"""
Configuration settings for the Capybara Sui Bot.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API Credentials
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Sui RPC URL
SUI_RPC_URL = os.getenv("SUI_RPC_URL", "https://sui-mainnet-rpc.allthatnode.com")

# List of Sui-related accounts to follow and analyze
SUI_ACCOUNTS = [
    # Core Team and Founders
    'b1ackd0g',
    'EvanWeb3',
    'EmanAbio',
    'Mysten_Labs',
    'SuiNetwork',
    'SuiChiefEcon',
    'SuiCorner',
    'Community_Sui',
    'NotCryptoBro',
    'NativeAssets',
    
    # Projects
    'WalrusProtocol',
    'CetusProtocol',
    'DeLoreanlabs',
    'KriyaDEX',
    'Turbos_finance',
    'bucket_protocol',
    'TypusFinance',
    'FlowX_finance',
    'doubleup_app',
    'sudofinance',
    'SuiPlay',
    'Scallop_io',
    'SuiNSdapp',
    'suipiens',
    'SuiAIFun'
]

# Memecoin communities to engage with
MEMECOIN_COMMUNITIES = [
    'lofitheyeti',
    'hippo_cto',
    'memeficlub',
    'Axolonsui',
    'blubsui',
    'fudthepug',
    'Piguworld',
    'zen_frogs'
]

# API endpoints
BLOCKVISION_API_BASE = os.getenv(
    "BLOCKVISION_API_BASE",
    "https://api.blockvision.org/v1"
)
SUIVISION_API_BASE = os.getenv(
    "SUIVISION_API_BASE",
    "https://api.suivision.io/v1"
)

# API keys (if needed)
BLOCKVISION_API_KEY = os.getenv("BLOCKVISION_API_KEY", "")
SUIVISION_API_KEY = os.getenv("SUIVISION_API_KEY", "")

# Price API settings
PRICE_UPDATE_INTERVAL = int(os.getenv("PRICE_UPDATE_INTERVAL", "60"))  # seconds
PRICE_HISTORY_DAYS = int(os.getenv("PRICE_HISTORY_DAYS", "7"))
PRICE_CHANGE_HOURS = int(os.getenv("PRICE_CHANGE_HOURS", "24"))

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Analysis Settings
TWEET_ANALYSIS_INTERVAL = 3600  # 1 hour in seconds
ONCHAIN_UPDATE_INTERVAL = 1800  # 30 minutes in seconds
MAX_TWEETS_PER_ACCOUNT = 10  # Number of tweets to analyze per account

# Engagement Settings
MAX_DAILY_TWEETS = 20
MAX_DAILY_REPLIES = 50
MIN_ENGAGEMENT_THRESHOLD = 5  # Minimum likes/retweets for a tweet to be considered significant
MEMECOIN_ENGAGEMENT_INTERVAL = 1800  # 30 minutes in seconds
MAX_MEMECOIN_REPLIES_PER_INTERVAL = 5  # Maximum number of memecoin community replies per interval

# Giveaway Settings
GIVEAWAY_INTERVAL = 86400  # 24 hours in seconds
MIN_ACTIVITY_SCORE = 100  # Minimum activity score to be eligible for giveaways
MAX_WINNERS_PER_GIVEAWAY = 5

# AI Settings
AI_MODEL = 'gpt-4'
MAX_TOKENS = 280  # Maximum tokens for tweet generation
TEMPERATURE = 0.7  # AI temperature for content generation

# Error Handling
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds 