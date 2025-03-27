"""Main bot module for Capybara Sui Bot."""

from typing import Dict, Optional
import asyncio
from loguru import logger
from pysui.sui.client import SuiClient
from pysui.sui.sui_config import SuiConfig

from .monitors import DeFiMonitor, PriceMonitor, CommunityManager

class CapybaraBot:
    """Main bot class that coordinates all monitoring and interaction tasks."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the bot with configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.sui_client = SuiClient(SuiConfig.default())
        self.defi_monitor = DeFiMonitor(self.sui_client)
        self.price_monitor = PriceMonitor()
        self.community_manager = CommunityManager()
        
        logger.info("Capybara Sui Bot initialized")
    
    async def start(self):
        """Start all monitoring tasks."""
        try:
            # Start monitors
            await asyncio.gather(
                self.defi_monitor.start(),
                self.price_monitor.start(),
                self.community_manager.start()
            )
            
            logger.info("All monitors started successfully")
            
            # Keep the bot running
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    async def stop(self):
        """Stop all monitoring tasks."""
        try:
            # Stop monitors
            await asyncio.gather(
                self.defi_monitor.stop(),
                self.price_monitor.stop(),
                self.community_manager.stop()
            )
            
            logger.info("All monitors stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            raise 