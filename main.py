import asyncio
import os
from dotenv import load_dotenv
from src.eliza.agents.capybara_agent import CapybaraAgent
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Verify required environment variables
        required_vars = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_TOKEN_SECRET",
            "OPENAI_API_KEY",
            "SUI_RPC_URL",
            "BLOCKVISION_API_KEY"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Initialize configuration
        config = {
            "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY"),
            "TWITTER_API_SECRET": os.getenv("TWITTER_API_SECRET"),
            "TWITTER_ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
            "TWITTER_ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "SUI_RPC_URL": os.getenv("SUI_RPC_URL"),
            "BLOCKVISION_API_KEY": os.getenv("BLOCKVISION_API_KEY"),
            "SUI_WALLET_ADDRESS": os.getenv("SUI_WALLET_ADDRESS"),
            "SUI_PRIVATE_KEY": os.getenv("SUI_PRIVATE_KEY")
        }
        
        # Create and run the Capybara agent
        agent = CapybaraAgent(config)
        await agent.run()
        
    except Exception as e:
        logger.error(f"Error running Capybara bot: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 