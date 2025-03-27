import pytest
import asyncio
from src.blockchain.sui_client import SuiClient

# Test token addresses (example addresses - replace with actual Sui token addresses)
TEST_TOKEN_ADDRESS = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
TEST_TOKEN_ADDRESSES = [
    "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
]

@pytest.mark.asyncio
async def test_get_token_price():
    async with SuiClient() as client:
        price = await client.get_token_price(TEST_TOKEN_ADDRESS)
        assert isinstance(price, float)
        assert price >= 0

@pytest.mark.asyncio
async def test_get_token_price_history():
    async with SuiClient() as client:
        history = await client.get_token_price_history(TEST_TOKEN_ADDRESS, days=7)
        assert isinstance(history, list)
        if history:  # If we have data
            assert isinstance(history[0], dict)
            assert "timestamp" in history[0]
            assert "price" in history[0]

@pytest.mark.asyncio
async def test_get_token_price_change():
    async with SuiClient() as client:
        change_data = await client.get_token_price_change(TEST_TOKEN_ADDRESS, hours=24)
        assert isinstance(change_data, dict)
        assert "price_change_percent" in change_data
        assert "current_price" in change_data
        assert isinstance(change_data["price_change_percent"], float)
        assert isinstance(change_data["current_price"], float)

@pytest.mark.asyncio
async def test_get_multiple_token_prices():
    async with SuiClient() as client:
        prices = await client.get_multiple_token_prices(TEST_TOKEN_ADDRESSES)
        assert isinstance(prices, dict)
        for addr, price in prices.items():
            assert addr in TEST_TOKEN_ADDRESSES
            assert isinstance(price, float)
            assert price >= 0

@pytest.mark.asyncio
async def test_get_price_alerts():
    async with SuiClient() as client:
        alert = await client.get_price_alerts(
            TEST_TOKEN_ADDRESS,
            price_target=1.0,
            is_above=True
        )
        assert isinstance(alert, dict)
        assert "status" in alert
        assert "message" in alert

@pytest.mark.asyncio
async def test_error_handling():
    async with SuiClient() as client:
        # Test with invalid token address
        price = await client.get_token_price("invalid_address")
        assert price == 0.0
        
        # Test with invalid days parameter
        history = await client.get_token_price_history(TEST_TOKEN_ADDRESS, days=-1)
        assert history == []
        
        # Test with empty token list
        prices = await client.get_multiple_token_prices([])
        assert prices == {} 