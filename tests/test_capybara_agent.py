import pytest
from unittest.mock import Mock, patch
from src.eliza.agents.capybara_agent import CapybaraAgent
from datetime import datetime

@pytest.fixture
def mock_config():
    return {
        "twitter": {
            "api_key": "test_key",
            "api_secret": "test_secret",
            "access_token": "test_token",
            "access_token_secret": "test_token_secret"
        },
        "sui": {
            "rpc_url": "test_url",
            "wallet_address": "test_address",
            "private_key": "test_key"
        },
        "blockvision": {
            "api_key": "test_key"
        },
        "bot": {
            "post_interval": 300,
            "giveaway_interval": 86400,
            "winners_count": 5,
            "reward_amount": 1000000,
            "reward_type": "sui"
        }
    }

@pytest.fixture
def mock_twitter_client():
    return Mock()

@pytest.fixture
def mock_sui_client():
    return Mock()

@pytest.fixture
async def capybara_agent(mock_config, mock_twitter_client, mock_sui_client):
    with patch("tweepy.API") as mock_api:
        mock_api.return_value = mock_twitter_client
        agent = CapybaraAgent(mock_config)
        agent.sui_client = mock_sui_client
        return agent

@pytest.mark.asyncio
async def test_analyze_sui_metrics(capybara_agent):
    """Test analyzing Sui metrics"""
    # Mock SuiTool response
    mock_sui_metrics = {
        "status": "success",
        "metrics": {
            "total_supply": 1000000,
            "active_accounts": 500
        }
    }
    capybara_agent.tools[0]._execute = Mock(return_value=mock_sui_metrics)

    # Mock BlockvisionTool response
    mock_blockvision_metrics = {
        "status": "success",
        "metrics": {
            "tvl_by_project": {"total": 1000000},
            "active_accounts": 500
        }
    }
    capybara_agent.tools[1]._execute = Mock(return_value=mock_blockvision_metrics)

    result = await capybara_agent._analyze_sui_metrics()
    assert result["status"] == "success"
    assert "metrics" in result
    assert "sui_metrics" in result["metrics"]
    assert "defi_metrics" in result["metrics"]

@pytest.mark.asyncio
async def test_generate_content(capybara_agent):
    """Test content generation"""
    # Mock metrics
    mock_metrics = {
        "status": "success",
        "metrics": {
            "sui_metrics": {
                "total_supply": 1000000
            },
            "defi_metrics": {
                "tvl_by_project": {"total": 1000000},
                "active_accounts": 500
            }
        }
    }
    
    with patch.object(capybara_agent, "_analyze_sui_metrics", return_value=mock_metrics):
        result = await capybara_agent._generate_content(type="general")
        assert result["status"] == "success"
        assert "content" in result
        assert "#SuiEcosystem" in result["content"]

@pytest.mark.asyncio
async def test_run_giveaway(capybara_agent):
    """Test giveaway execution"""
    # Mock GiveawayTool responses
    mock_winners = {
        "status": "success",
        "winners": ["user1", "user2", "user3"]
    }
    mock_distribution = {
        "status": "success",
        "distributions": [
            {"winner": "user1", "status": "success"},
            {"winner": "user2", "status": "success"},
            {"winner": "user3", "status": "success"}
        ]
    }
    
    capybara_agent.tools[2]._execute = Mock(side_effect=[mock_winners, mock_distribution])
    
    result = await capybara_agent._run_giveaway()
    assert result["status"] == "success"
    assert "winners" in result
    assert "distributions" in result

@pytest.mark.asyncio
async def test_calculate_tweet_quality(capybara_agent):
    """Test tweet quality calculation"""
    # Test with various tweet types
    tweets = {
        "Good tweet with hashtags": "#SuiEcosystem is great for #DeFi and #NFTs",
        "Question tweet": "How does Sui handle transaction finality?",
        "Short tweet": "hi",
        "Positive sentiment": "This is an amazing development for Sui!"
    }
    
    for tweet_text, content in tweets.items():
        score = capybara_agent.tools[2]._calculate_tweet_quality(content)
        assert isinstance(score, float)
        assert 0 <= score <= 5.0 