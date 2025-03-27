import asyncio
import yaml
import logging
from dotenv import load_dotenv
import os
from src.eliza.agents.capybara_agent import CapybaraAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from YAML file"""
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise

async def main():
    """Main function to run the bot"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        config = load_config()
        
        # Create and run the Capybara agent
        agent = CapybaraAgent(config)
        await agent.run()
        
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 