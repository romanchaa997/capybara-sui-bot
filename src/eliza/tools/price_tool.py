from typing import Dict, Any, Optional
import httpx
import logging
from datetime import datetime, timedelta
from ..base import Tool
from ..data.sui_projects import TOKEN_INFO

class PriceTool(Tool):
    def __init__(self):
        super().__init__(
            name="price_data",
            description="Fetches and processes token price data",
            function=self._execute  # Pass the _execute method as the function
        )
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
        
        # API endpoints for different data sources
        self.endpoints = {
            "coingecko": "https://api.coingecko.com/api/v3",
            "binance": "https://api.binance.com/api/v3",
            "sui": "https://fullnode.mainnet.sui.io:443"
        }

    async def _execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute price data actions"""
        try:
            if action == "get_price":
                return await self._get_token_price(kwargs.get("token", ""))
            elif action == "get_market_data":
                return await self._get_market_data(kwargs.get("token", ""))
            else:
                raise ValueError(f"Unknown action: {action}")
        except Exception as e:
            self.logger.error(f"Error executing price data action: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _get_token_price(self, token: str) -> Dict[str, Any]:
        """Get token price data from multiple sources"""
        try:
            # Check cache first
            if token in self.cache:
                cache_data = self.cache[token]
                if datetime.now() - cache_data["timestamp"] < self.cache_duration:
                    return cache_data["data"]

            # Get token info
            token_info = TOKEN_INFO.get(token.lower())
            if not token_info:
                return {"status": "error", "message": f"Unknown token: {token}"}

            # Fetch price data from multiple sources
            async with httpx.AsyncClient() as client:
                # Try CoinGecko first
                try:
                    coingecko_data = await self._fetch_coingecko_data(client, token_info)
                    if coingecko_data["status"] == "success":
                        return self._cache_and_return(token, coingecko_data)
                except Exception as e:
                    self.logger.warning(f"CoinGecko fetch failed: {str(e)}")

                # Try Binance as fallback
                try:
                    binance_data = await self._fetch_binance_data(client, token_info)
                    if binance_data["status"] == "success":
                        return self._cache_and_return(token, binance_data)
                except Exception as e:
                    self.logger.warning(f"Binance fetch failed: {str(e)}")

                # Try Sui RPC as last resort
                try:
                    sui_data = await self._fetch_sui_data(client, token_info)
                    if sui_data["status"] == "success":
                        return self._cache_and_return(token, sui_data)
                except Exception as e:
                    self.logger.warning(f"Sui RPC fetch failed: {str(e)}")

            return {"status": "error", "message": "Failed to fetch price data from all sources"}
        except Exception as e:
            self.logger.error(f"Error getting token price: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _fetch_coingecko_data(self, client: httpx.AsyncClient, token_info: Dict[str, str]) -> Dict[str, Any]:
        """Fetch price data from CoinGecko"""
        try:
            # Map token symbols to CoinGecko IDs
            coingecko_ids = {
                "sui": "sui",
                "cetus": "cetus",
                "navi": "navi-protocol"
            }
            
            coingecko_id = coingecko_ids.get(token_info["name"].lower())
            if not coingecko_id:
                return {"status": "error", "message": "Token not found on CoinGecko"}

            response = await client.get(
                f"{self.endpoints['coingecko']}/simple/price",
                params={
                    "ids": coingecko_id,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                    "include_market_cap": "true"
                }
            )
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "price": data[coingecko_id]["usd"],
                "change": data[coingecko_id]["usd_24h_change"],
                "mcap": data[coingecko_id]["usd_market_cap"]
            }
        except Exception as e:
            self.logger.error(f"Error fetching CoinGecko data: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _fetch_binance_data(self, client: httpx.AsyncClient, token_info: Dict[str, str]) -> Dict[str, Any]:
        """Fetch price data from Binance"""
        try:
            # Map token symbols to Binance symbols
            binance_symbols = {
                "sui": "SUIUSDT",
                "cetus": "CETUSUSDT",
                "navi": "NAVIUSDT"
            }
            
            symbol = binance_symbols.get(token_info["name"].upper())
            if not symbol:
                return {"status": "error", "message": "Token not found on Binance"}

            response = await client.get(
                f"{self.endpoints['binance']}/ticker/24hr",
                params={"symbol": symbol}
            )
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "price": float(data["lastPrice"]),
                "change": float(data["priceChangePercent"]),
                "mcap": float(data["quoteVolume"])  # Using 24h volume as proxy for market cap
            }
        except Exception as e:
            self.logger.error(f"Error fetching Binance data: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _fetch_sui_data(self, client: httpx.AsyncClient, token_info: Dict[str, str]) -> Dict[str, Any]:
        """Fetch price data from Sui RPC"""
        try:
            # This is a simplified version - in reality, you'd need to:
            # 1. Get the token's pool address from a DEX
            # 2. Query the pool's reserves
            # 3. Calculate the price based on reserves
            response = await client.post(
                self.endpoints["sui"],
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "suix_getLatestCheckpoint",
                    "params": []
                }
            )
            response.raise_for_status()
            
            # For now, return placeholder data
            return {
                "status": "success",
                "price": "0.00",
                "change": "0.00",
                "mcap": "0.00"
            }
        except Exception as e:
            self.logger.error(f"Error fetching Sui RPC data: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _cache_and_return(self, token: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cache the data and return it"""
        self.cache[token] = {
            "data": data,
            "timestamp": datetime.now()
        }
        return data

    async def _get_market_data(self, token: str) -> Dict[str, Any]:
        """Get comprehensive market data for a token"""
        try:
            price_data = await self._get_token_price(token)
            if price_data["status"] != "success":
                return price_data

            # Add additional market data
            return {
                "status": "success",
                "price_data": price_data,
                "market_metrics": {
                    "volume_24h": "0.00",  # Would be fetched from exchange APIs
                    "liquidity": "0.00",   # Would be fetched from DEX pools
                    "holders": "0",        # Would be fetched from blockchain
                    "market_rank": "0"     # Would be fetched from market data providers
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting market data: {str(e)}")
            return {"status": "error", "message": str(e)} 