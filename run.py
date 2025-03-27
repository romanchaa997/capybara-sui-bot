#!/usr/bin/env python3
"""Main entry point for Capybara Sui Bot."""

import asyncio
import signal
from loguru import logger
from dotenv import load_dotenv

from capybara_sui_bot import CapybaraBot

async def main():
    """Main function to run the bot."""
    # Load environment variables
    load_dotenv()
    
    # Initialize bot
    bot = CapybaraBot()
    
    # Handle graceful shutdown
    def shutdown(signal, frame):
        logger.info("Shutting down...")
        asyncio.create_task(bot.stop())
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    try:
        # Start bot
        await bot.start()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 