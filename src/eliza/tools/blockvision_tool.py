from typing import Dict, Any, List
import aiohttp
import logging
from datetime import datetime, timedelta
from ..base import Tool

class BlockvisionTool(Tool):
    def __init__(self, api_key: str):
        super().__init__(
            name="blockvision_analytics",
            description="Analyze Sui blockchain data using Blockvision API for market insights and analytics",
            function=self._execute
        )
        self.api_key = api_key
        self.base_url = "https://api.blockvision.org/v1"
        self.logger = logging.getLogger(__name__)

    async def _execute(self, **kwargs) -> Dict[str, Any]:
        """Execute Blockvision analytics operations"""
        try:
            action = kwargs.get("action", "get_market_data")
            
            if action == "get_market_data":
                return await self._get_market_data()
            elif action == "get_token_metrics":
                return await self._get_token_metrics(kwargs.get("token_id"))
            elif action == "get_protocol_metrics":
                return await self._get_protocol_metrics(kwargs.get("protocol"))
            elif action == "get_whale_activity":
                return await self._get_whale_activity()
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
                
        except Exception as e:
            self.logger.error(f"Error executing Blockvision tool: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _get_market_data(self) -> Dict[str, Any]:
        """Get overall market data for Sui ecosystem"""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.get(
                f"{self.base_url}/market/overview",
                headers=headers
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "market_data": {
                        "total_market_cap": data.get("total_market_cap"),
                        "24h_volume": data.get("volume_24h"),
                        "active_protocols": data.get("active_protocols"),
                        "total_value_locked": data.get("tvl"),
                        "market_trends": data.get("trends")
                    }
                }

    async def _get_token_metrics(self, token_id: str) -> Dict[str, Any]:
        """Get detailed metrics for a specific token"""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.get(
                f"{self.base_url}/tokens/{token_id}/metrics",
                headers=headers
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "token_metrics": {
                        "price": data.get("price"),
                        "market_cap": data.get("market_cap"),
                        "volume_24h": data.get("volume_24h"),
                        "holders": data.get("holders"),
                        "price_change_24h": data.get("price_change_24h"),
                        "liquidity": data.get("liquidity")
                    }
                }

    async def _get_protocol_metrics(self, protocol: str) -> Dict[str, Any]:
        """Get metrics for a specific protocol"""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.get(
                f"{self.base_url}/protocols/{protocol}/metrics",
                headers=headers
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "protocol_metrics": {
                        "tvl": data.get("tvl"),
                        "volume_24h": data.get("volume_24h"),
                        "users_24h": data.get("users_24h"),
                        "fees_24h": data.get("fees_24h"),
                        "revenue_24h": data.get("revenue_24h")
                    }
                }

    async def _get_whale_activity(self) -> Dict[str, Any]:
        """Get recent whale activity on Sui"""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.get(
                f"{self.base_url}/whales/activity",
                headers=headers
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "whale_activity": {
                        "large_transactions": data.get("large_transactions"),
                        "whale_movements": data.get("whale_movements"),
                        "accumulation_trends": data.get("accumulation_trends")
                    }
                } 