import asyncio
import pytest
from src.eliza.tools.community_tool import CommunityTool
from src.eliza.tools.sui_tool import SuiTool
from src.eliza.tools.blockvision_tool import BlockvisionTool
from src.eliza.tools.giveaway_tool import GiveawayTool
from unittest.mock import Mock, patch

@pytest.fixture
def mock_twitter():
    return Mock()

@pytest.fixture
def mock_sui_client():
    return Mock()

@pytest.fixture
def mock_blockvision():
    return Mock()

async def test_community_tool(mock_twitter):
    community_tool = CommunityTool(mock_twitter)
    
    # Test basic queries
    test_queries = [
        "what's the price of sui?",
        "tell me about cetus",
        "how does staking work?",
        "what defi protocols are on sui?",
        "what's the contract for sui token?",
        "what projects are building on sui?",
        "show me a meme",
        "random text that doesn't match any pattern"
    ]
    
    for query in test_queries:
        result = await community_tool._handle_specific_query(query)
        assert "status" in result
        assert "response" in result or "message" in result

    # Test sentiment analysis
    test_sentiments = [
        "Sui is amazing! 🚀",
        "I'm not sure about this...",
        "This is terrible! 😡",
        "",  # Empty string
        "a" * 1000  # Very long string
    ]
    
    for text in test_sentiments:
        result = await community_tool._analyze_sentiment(text)
        assert "sentiment" in result
        assert "score" in result

async def test_sui_tool(mock_sui_client):
    sui_tool = SuiTool(mock_sui_client)
    
    # Test price fetching
    with patch('src.eliza.tools.sui_tool.SuiTool._fetch_price') as mock_fetch:
        mock_fetch.return_value = {"price": 1.23, "change_24h": 5.6}
        result = await sui_tool.get_token_price("SUI")
        assert result["status"] == "success"
        assert "price" in result["response"]
    
    # Test error handling
    with patch('src.eliza.tools.sui_tool.SuiTool._fetch_price') as mock_fetch:
        mock_fetch.side_effect = Exception("API Error")
        result = await sui_tool.get_token_price("SUI")
        assert result["status"] == "error"
        assert "message" in result

async def test_blockvision_tool(mock_blockvision):
    blockvision_tool = BlockvisionTool(mock_blockvision)
    
    # Test market data
    with patch('src.eliza.tools.blockvision_tool.BlockvisionTool._fetch_market_data') as mock_fetch:
        mock_fetch.return_value = {"volume": 1000000, "market_cap": 50000000}
        result = await blockvision_tool.get_market_data("SUI")
        assert result["status"] == "success"
        assert "volume" in result["response"]
    
    # Test protocol metrics
    with patch('src.eliza.tools.blockvision_tool.BlockvisionTool._fetch_protocol_metrics') as mock_fetch:
        mock_fetch.return_value = {"tvl": 1000000, "apy": 15.5}
        result = await blockvision_tool.get_protocol_metrics("CETUS")
        assert result["status"] == "success"
        assert "tvl" in result["response"]

async def test_giveaway_tool():
    giveaway_tool = GiveawayTool()
    
    # Test giveaway creation
    with patch('src.eliza.tools.giveaway_tool.GiveawayTool._create_giveaway') as mock_create:
        mock_create.return_value = {"id": "123", "status": "created"}
        result = await giveaway_tool.create_giveaway(
            prize="100 SUI",
            duration_hours=24,
            requirements={"min_followers": 100}
        )
        assert result["status"] == "success"
        assert "id" in result["response"]
    
    # Test winner selection
    with patch('src.eliza.tools.giveaway_tool.GiveawayTool._select_winners') as mock_select:
        mock_select.return_value = ["user1", "user2"]
        result = await giveaway_tool.select_winners("123", 2)
        assert result["status"] == "success"
        assert len(result["response"]) == 2

@pytest.mark.asyncio
async def test_integration():
    # Test full integration between tools
    community_tool = CommunityTool(Mock())
    sui_tool = SuiTool(Mock())
    blockvision_tool = BlockvisionTool(Mock())
    giveaway_tool = GiveawayTool()
    
    # Test a complex query that requires multiple tools
    query = "What's the current SUI price and TVL of Cetus?"
    
    # Mock responses
    with patch('src.eliza.tools.sui_tool.SuiTool._fetch_price') as mock_price, \
         patch('src.eliza.tools.blockvision_tool.BlockvisionTool._fetch_protocol_metrics') as mock_metrics:
        
        mock_price.return_value = {"price": 1.23, "change_24h": 5.6}
        mock_metrics.return_value = {"tvl": 1000000, "apy": 15.5}
        
        result = await community_tool._handle_specific_query(query)
        assert result["status"] == "success"
        assert "price" in result["response"].lower()
        assert "tvl" in result["response"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 