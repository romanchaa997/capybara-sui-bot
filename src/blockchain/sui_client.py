import aiohttp
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
from src.config.settings import (
    SUI_RPC_URL,
    BLOCKVISION_API_BASE,
    SUIVISION_API_BASE
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SuiClient:
    def __init__(self):
        """Initialize Sui blockchain client."""
        self.session = None
        self.rpc_url = SUI_RPC_URL
        self.blockvision_api = BLOCKVISION_API_BASE
        self.suivision_api = SUIVISION_API_BASE

    async def __aenter__(self):
        """Initialize aiohttp session."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session."""
        if self.session:
            await self.session.close()

    async def get_tvl_by_project(self) -> List[Dict[str, Any]]:
        """Get TVL data for all Sui projects."""
        try:
            async with self.session.get(f"{self.suivision_api}/defi/tvl") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('projects', [])
                else:
                    logger.error(f"Failed to fetch TVL data: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching TVL data: {str(e)}")
            return []

    async def get_top_projects(self) -> List[Dict[str, Any]]:
        """Get top Sui projects by volume."""
        try:
            async with self.session.get(f"{self.suivision_api}/defi/projects") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('projects', [])
                else:
                    logger.error(f"Failed to fetch top projects: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching top projects: {str(e)}")
            return []

    async def get_trading_pairs(self) -> List[Dict[str, Any]]:
        """Get top trading pairs on Sui."""
        try:
            async with self.session.get(f"{self.suivision_api}/coins/pairs") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('pairs', [])
                else:
                    logger.error(f"Failed to fetch trading pairs: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching trading pairs: {str(e)}")
            return []

    async def get_farming_pools(self) -> List[Dict[str, Any]]:
        """Get top farming pools on Sui."""
        try:
            async with self.session.get(f"{self.suivision_api}/defi/pools") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('pools', [])
                else:
                    logger.error(f"Failed to fetch farming pools: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching farming pools: {str(e)}")
            return []

    async def get_nft_collections(self) -> List[Dict[str, Any]]:
        """Get top NFT collections by volume."""
        try:
            async with self.session.get(f"{self.suivision_api}/nfts/collections") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('collections', [])
                else:
                    logger.error(f"Failed to fetch NFT collections: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching NFT collections: {str(e)}")
            return []

    async def get_network_metrics(self) -> Dict[str, Any]:
        """Get overall network metrics."""
        try:
            async with self.session.get(f"{self.blockvision_api}/network/metrics") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch network metrics: {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error fetching network metrics: {str(e)}")
            return {}

    async def get_active_accounts(self, hours: int = 24) -> int:
        """Get number of active accounts in the last specified hours."""
        try:
            async with self.session.get(f"{self.blockvision_api}/network/active-accounts") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('active_accounts', 0)
                else:
                    logger.error(f"Failed to fetch active accounts: {response.status}")
                    return 0
        except Exception as e:
            logger.error(f"Error fetching active accounts: {str(e)}")
            return 0

    async def get_transaction_count(self, hours: int = 24) -> int:
        """Get number of transactions in the last specified hours."""
        try:
            async with self.session.get(f"{self.blockvision_api}/network/transactions") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('transaction_count', 0)
                else:
                    logger.error(f"Failed to fetch transaction count: {response.status}")
                    return 0
        except Exception as e:
            logger.error(f"Error fetching transaction count: {str(e)}")
            return 0

    async def get_token_price(self, token_address: str) -> float:
        """Get current price of a specific token."""
        try:
            async with self.session.get(f"{self.suivision_api}/coins/price/{token_address}") as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data.get('price', 0))
                else:
                    logger.error(f"Failed to fetch token price: {response.status}")
                    return 0.0
        except Exception as e:
            logger.error(f"Error fetching token price: {str(e)}")
            return 0.0

    async def get_token_price_history(self, token_address: str, days: int = 7) -> List[Dict[str, Any]]:
        """Get historical price data for a token.
        
        Args:
            token_address: The token's contract address
            days: Number of days of historical data to fetch
            
        Returns:
            List of dicts containing timestamp and price data
        """
        try:
            async with self.session.get(
                f"{self.suivision_api}/coins/price/history/{token_address}",
                params={"days": days}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('history', [])
                else:
                    logger.error(f"Failed to fetch token price history: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching token price history: {str(e)}")
            return []

    async def get_token_price_change(self, token_address: str, hours: int = 24) -> Dict[str, float]:
        """Get price change percentage for a token over specified hours.
        
        Args:
            token_address: The token's contract address
            hours: Time period in hours
            
        Returns:
            Dict containing price change percentage and current price
        """
        try:
            async with self.session.get(
                f"{self.suivision_api}/coins/price/change/{token_address}",
                params={"hours": hours}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "price_change_percent": float(data.get('price_change_percent', 0)),
                        "current_price": float(data.get('current_price', 0))
                    }
                else:
                    logger.error(f"Failed to fetch token price change: {response.status}")
                    return {"price_change_percent": 0, "current_price": 0}
        except Exception as e:
            logger.error(f"Error fetching token price change: {str(e)}")
            return {"price_change_percent": 0, "current_price": 0}

    async def get_multiple_token_prices(self, token_addresses: List[str]) -> Dict[str, float]:
        """Get current prices for multiple tokens in a single API call.
        
        Args:
            token_addresses: List of token contract addresses
            
        Returns:
            Dict mapping token addresses to their current prices
        """
        try:
            async with self.session.post(
                f"{self.suivision_api}/coins/prices/batch",
                json={"tokens": token_addresses}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {addr: float(price) for addr, price in data.get('prices', {}).items()}
                else:
                    logger.error(f"Failed to fetch multiple token prices: {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error fetching multiple token prices: {str(e)}")
            return {}

    async def get_price_alerts(self, token_address: str, price_target: float, 
                             is_above: bool = True) -> Dict[str, Any]:
        """Set up a price alert for a token.
        
        Args:
            token_address: The token's contract address
            price_target: Target price to monitor
            is_above: True to alert when price goes above target, False for below
            
        Returns:
            Dict containing alert status and details
        """
        try:
            async with self.session.post(
                f"{self.suivision_api}/coins/price/alert",
                json={
                    "token_address": token_address,
                    "price_target": price_target,
                    "is_above": is_above
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to set price alert: {response.status}")
                    return {"status": "error", "message": "Failed to set alert"}
        except Exception as e:
            logger.error(f"Error setting price alert: {str(e)}")
            return {"status": "error", "message": str(e)} 