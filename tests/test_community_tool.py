import pytest
import asyncio
from unittest.mock import Mock, patch
from src.eliza.tools.community_tool import CommunityTool
from src.eliza.tools.price_tool import PriceTool

@pytest.fixture
def mock_twitter_client():
    return Mock()

@pytest.fixture
def community_tool(mock_twitter_client):
    return CommunityTool(mock_twitter_client)

@pytest.mark.asyncio
async def test_price_query(community_tool):
    # Mock price data
    mock_price_data = {
        "status": "success",
        "price": "1.23",
        "change": "5.67",
        "mcap": "1000000"
    }
    
    with patch.object(PriceTool, '_execute', return_value=mock_price_data):
        result = await community_tool._handle_specific_query("what's the price of sui?")
        
        assert result["status"] == "success"
        assert result["type"] == "price_query"
        assert "1.23" in result["response"]
        assert "5.67" in result["response"]
        assert "1000000" in result["response"]

@pytest.mark.asyncio
async def test_project_info(community_tool):
    result = await community_tool._handle_specific_query("tell me about cetus")
    
    assert result["status"] == "success"
    assert result["type"] == "project_info"
    assert "Cetus" in result["response"]
    assert "DEX" in result["response"]
    assert "liquidity" in result["response"]

@pytest.mark.asyncio
async def test_technical_query(community_tool):
    result = await community_tool._handle_specific_query("how does staking work?")
    
    assert result["status"] == "success"
    assert result["type"] == "technical"
    assert "staking" in result["response"].lower()
    assert "rewards" in result["response"].lower()

@pytest.mark.asyncio
async def test_defi_query(community_tool):
    result = await community_tool._handle_specific_query("what defi protocols are on sui?")
    
    assert result["status"] == "success"
    assert result["type"] == "defi"
    assert "protocols" in result["response"].lower()
    assert "Cetus" in result["response"]
    assert "Navi" in result["response"]

@pytest.mark.asyncio
async def test_token_info(community_tool):
    result = await community_tool._handle_specific_query("what's the contract for sui token?")
    
    assert result["status"] == "success"
    assert result["type"] == "token_info"
    assert "0x2::sui::SUI" in result["response"]

@pytest.mark.asyncio
async def test_sentiment_analysis(community_tool):
    result = await community_tool._analyze_sentiment("Sui is amazing! 🚀")
    
    assert result["status"] == "success"
    assert result["sentiment"] == "positive"
    assert result["score"] > 0

@pytest.mark.asyncio
async def test_ecosystem_query(community_tool):
    result = await community_tool._handle_specific_query("what projects are building on sui?")
    
    assert result["status"] == "success"
    assert result["type"] == "ecosystem"
    assert "Cetus" in result["response"]
    assert "Navi" in result["response"]
    assert "Aftermath" in result["response"]

@pytest.mark.asyncio
async def test_meme_request(community_tool):
    result = await community_tool._handle_specific_query("show me a meme")
    
    assert result["status"] == "success"
    assert result["type"] == "meme"
    assert "🚀" in result["response"]

@pytest.mark.asyncio
async def test_unknown_query(community_tool):
    result = await community_tool._handle_specific_query("random text that doesn't match any pattern")
    
    assert result["status"] == "error"
    assert "No specific query pattern matched" in result["message"]

@pytest.mark.asyncio
async def test_monitor_mentions(community_tool, mock_twitter_client):
    # Mock mentions
    mock_mention = Mock()
    mock_mention.id = 123
    mock_mention.text = "what's the price of sui?"
    mock_mention.user.screen_name = "test_user"
    mock_twitter_client.get_mentions_timeline.return_value = [mock_mention]
    
    # Mock price data
    mock_price_data = {
        "status": "success",
        "price": "1.23",
        "change": "5.67",
        "mcap": "1000000"
    }
    
    with patch.object(PriceTool, '_execute', return_value=mock_price_data):
        result = await community_tool._monitor_mentions()
        
        assert result["status"] == "success"
        assert len(result["processed_mentions"]) == 1
        assert result["processed_mentions"][0]["tweet_id"] == 123
        assert result["processed_mentions"][0]["user"] == "test_user"
        assert result["processed_mentions"][0]["sentiment"] == "neutral"
        
        # Verify that update_status was called
        mock_twitter_client.update_status.assert_called_once()

@pytest.mark.asyncio
async def test_track_engagement(community_tool):
    # Add some test engagement history
    community_tool.engagement_history = [
        {"sentiment": "positive", "response": "test response"},
        {"sentiment": "negative", "response": "test response"},
        {"sentiment": "neutral", "response": "test response"}
    ]
    
    result = await community_tool._track_engagement()
    
    assert result["status"] == "success"
    assert result["metrics"]["total_mentions"] == 3
    assert result["metrics"]["sentiment_distribution"]["positive"] == 1
    assert result["metrics"]["sentiment_distribution"]["negative"] == 1
    assert result["metrics"]["sentiment_distribution"]["neutral"] == 1
    assert result["metrics"]["response_rate"] == 100.0 