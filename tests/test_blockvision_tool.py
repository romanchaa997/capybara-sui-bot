import pytest
import aiohttp
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from src.eliza.tools.blockvision_tool import BlockvisionTool

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {
        "total_market_cap": 1000000000,
        "volume_24h": 50000000,
        "active_protocols": 10,
        "tvl": 200000000,
        "trends": {"price": "up", "volume": "up"}
    }
    return mock

@pytest.fixture
def blockvision_tool():
    return BlockvisionTool(api_key="test_api_key")

@pytest.mark.asyncio
async def test_get_market_data(blockvision_tool, mock_response):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        result = await blockvision_tool._execute(action="get_market_data")
        
        assert result["status"] == "success"
        assert "market_data" in result
        assert result["market_data"]["total_market_cap"] == 1000000000
        assert result["market_data"]["volume_24h"] == 50000000

@pytest.mark.asyncio
async def test_get_token_metrics(blockvision_tool):
    mock_token_response = Mock()
    mock_token_response.json.return_value = {
        "price": 1.5,
        "market_cap": 750000000,
        "volume_24h": 25000000,
        "holders": 10000,
        "price_change_24h": 5.2,
        "liquidity": 10000000
    }
    
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_token_response
        
        result = await blockvision_tool._execute(
            action="get_token_metrics",
            token_id="test_token_id"
        )
        
        assert result["status"] == "success"
        assert "token_metrics" in result
        assert result["token_metrics"]["price"] == 1.5
        assert result["token_metrics"]["holders"] == 10000

@pytest.mark.asyncio
async def test_get_protocol_metrics(blockvision_tool):
    mock_protocol_response = Mock()
    mock_protocol_response.json.return_value = {
        "tvl": 50000000,
        "volume_24h": 10000000,
        "users_24h": 1000,
        "fees_24h": 50000,
        "revenue_24h": 100000
    }
    
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_protocol_response
        
        result = await blockvision_tool._execute(
            action="get_protocol_metrics",
            protocol="test_protocol"
        )
        
        assert result["status"] == "success"
        assert "protocol_metrics" in result
        assert result["protocol_metrics"]["tvl"] == 50000000
        assert result["protocol_metrics"]["users_24h"] == 1000

@pytest.mark.asyncio
async def test_get_whale_activity(blockvision_tool):
    mock_whale_response = Mock()
    mock_whale_response.json.return_value = {
        "large_transactions": [
            {"amount": 1000000, "timestamp": "2024-03-27T12:00:00Z"}
        ],
        "whale_movements": [
            {"from": "wallet1", "to": "wallet2", "amount": 500000}
        ],
        "accumulation_trends": {"trend": "increasing", "period": "24h"}
    }
    
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_whale_response
        
        result = await blockvision_tool._execute(action="get_whale_activity")
        
        assert result["status"] == "success"
        assert "whale_activity" in result
        assert len(result["whale_activity"]["large_transactions"]) == 1
        assert result["whale_activity"]["accumulation_trends"]["trend"] == "increasing"

@pytest.mark.asyncio
async def test_error_handling(blockvision_tool):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.side_effect = Exception("API Error")
        
        result = await blockvision_tool._execute(action="get_market_data")
        
        assert result["status"] == "error"
        assert "message" in result
        assert "API Error" in result["message"]

@pytest.mark.asyncio
async def test_unknown_action(blockvision_tool):
    result = await blockvision_tool._execute(action="unknown_action")
    
    assert result["status"] == "error"
    assert "Unknown action" in result["message"]

@pytest.mark.asyncio
async def test_rate_limit_handling(blockvision_tool):
    mock_response = Mock()
    mock_response.status = 429
    mock_response.json.return_value = {"error": "Rate limit exceeded"}
    
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        result = await blockvision_tool._execute(action="get_market_data")
        
        assert result["status"] == "error"
        assert "Rate limit exceeded" in result["message"]

@pytest.mark.asyncio
async def test_invalid_token_id(blockvision_tool):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.status = 404
        
        result = await blockvision_tool._execute(
            action="get_token_metrics",
            token_id="invalid_token"
        )
        
        assert result["status"] == "error"
        assert "Token not found" in result["message"]

@pytest.mark.asyncio
async def test_invalid_protocol(blockvision_tool):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.status = 404
        
        result = await blockvision_tool._execute(
            action="get_protocol_metrics",
            protocol="invalid_protocol"
        )
        
        assert result["status"] == "error"
        assert "Protocol not found" in result["message"]

@pytest.mark.asyncio
async def test_missing_api_key(blockvision_tool):
    blockvision_tool.api_key = None
    
    result = await blockvision_tool._execute(action="get_market_data")
    
    assert result["status"] == "error"
    assert "API key not configured" in result["message"]

@pytest.mark.asyncio
async def test_invalid_response_format(blockvision_tool):
    mock_response = Mock()
    mock_response.json.return_value = {"invalid": "format"}
    
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        result = await blockvision_tool._execute(action="get_market_data")
        
        assert result["status"] == "error"
        assert "Invalid response format" in result["message"] 