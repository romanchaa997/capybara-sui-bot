from typing import Dict, Any
import aiohttp
import json
import logging
from ..base import Tool

class SuiTool(Tool):
    def __init__(self, rpc_url: str):
        super().__init__(
            name="sui_blockchain",
            description="Interact with the Sui blockchain to fetch data and analyze on-chain activity",
            function=self._execute
        )
        self.rpc_url = rpc_url
        self.logger = logging.getLogger(__name__)

    async def _execute(self, **kwargs) -> Dict[str, Any]:
        """Execute Sui blockchain operations"""
        try:
            action = kwargs.get("action", "get_metrics")
            
            if action == "get_metrics":
                return await self._get_metrics()
            elif action == "get_recent_transactions":
                return await self._get_recent_transactions()
            elif action == "get_token_price":
                return await self._get_token_price(kwargs.get("token_id"))
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
                
        except Exception as e:
            self.logger.error(f"Error executing Sui tool: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _get_metrics(self) -> Dict[str, Any]:
        """Get Sui blockchain metrics"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "sui_getTotalSupply",
                    "params": []
                }
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "metrics": {
                        "total_supply": data.get("result", "Unknown"),
                        "timestamp": data.get("timestamp", "Unknown")
                    }
                }

    async def _get_recent_transactions(self) -> Dict[str, Any]:
        """Get recent transactions"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "sui_getRecentTransactions",
                    "params": [10]  # Get last 10 transactions
                }
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "transactions": data.get("result", [])
                }

    async def _get_token_price(self, token_id: str) -> Dict[str, Any]:
        """Get token price"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "sui_getTokenPrice",
                    "params": [token_id]
                }
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "price": data.get("result", "Unknown")
                } 