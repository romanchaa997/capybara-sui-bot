import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from src.eliza.tools.giveaway_tool import GiveawayTool

@pytest.fixture
def mock_sui_client():
    mock = Mock()
    mock.execute.return_value.id = "test_tx_id"
    return mock

@pytest.fixture
def mock_twitter_client():
    mock = Mock()
    mock.update_status.return_value = Mock(id="test_tweet_id")
    mock.user_timeline.return_value = [Mock(id="test_tweet_id")]
    return mock

@pytest.fixture
def giveaway_tool(mock_sui_client, mock_twitter_client):
    return GiveawayTool(
        sui_client=mock_sui_client,
        wallet_address="test_wallet",
        private_key="test_private_key",
        twitter_client=mock_twitter_client
    )

@pytest.mark.asyncio
async def test_create_giveaway(giveaway_tool, mock_sui_client, mock_twitter_client):
    token_id = "test_token"
    amount = 1000
    requirements = {"description": "Follow and RT"}
    
    result = await giveaway_tool._execute(
        action="create_giveaway",
        token_id=token_id,
        amount=amount,
        requirements=requirements
    )
    
    assert result["status"] == "success"
    assert result["giveaway_id"] == "test_tx_id"
    assert result["tweet_id"] == "test_tweet_id"
    
    # Verify Sui client was called correctly
    mock_sui_client.execute.assert_called_once()
    call_args = mock_sui_client.execute.call_args[0]
    assert call_args[0] == "create_giveaway"
    assert isinstance(call_args[1][0], dict)
    assert call_args[1][0]["token_id"] == token_id
    assert call_args[1][0]["amount"] == amount
    
    # Verify Twitter announcement
    mock_twitter_client.update_status.assert_called_once()
    tweet_text = mock_twitter_client.update_status.call_args[0][0]
    assert "New Giveaway Alert" in tweet_text
    assert str(amount) in tweet_text

@pytest.mark.asyncio
async def test_end_giveaway(giveaway_tool, mock_sui_client):
    giveaway_id = "test_giveaway_id"
    
    result = await giveaway_tool._execute(
        action="end_giveaway",
        giveaway_id=giveaway_id
    )
    
    assert result["status"] == "success"
    assert result["transaction_id"] == "test_tx_id"
    
    mock_sui_client.execute.assert_called_once_with(
        "end_giveaway",
        [giveaway_id],
        "test_wallet",
        "test_private_key"
    )

@pytest.mark.asyncio
async def test_select_winners(giveaway_tool, mock_sui_client):
    giveaway_id = "test_giveaway_id"
    mock_participants = ["user1", "user2", "user3", "user4", "user5"]
    
    # Mock the get_participants call
    mock_sui_client.execute.side_effect = [
        mock_participants,  # First call returns participants
        None  # Second call for store_winners
    ]
    
    result = await giveaway_tool._execute(
        action="select_winners",
        giveaway_id=giveaway_id
    )
    
    assert result["status"] == "success"
    assert len(result["winners"]) == 5  # Should select 5 winners
    assert result["transaction_id"] == "test_tx_id"
    
    # Verify Sui client calls
    assert mock_sui_client.execute.call_count == 2
    assert mock_sui_client.execute.call_args_list[0][0][0] == "get_participants"
    assert mock_sui_client.execute.call_args_list[1][0][0] == "store_winners"

@pytest.mark.asyncio
async def test_distribute_rewards(giveaway_tool, mock_sui_client, mock_twitter_client):
    giveaway_id = "test_giveaway_id"
    mock_winners = ["winner1", "winner2", "winner3"]
    
    # Mock the get_winners call
    mock_sui_client.execute.side_effect = [
        mock_winners,  # First call returns winners
        Mock(id="tx1"),  # Second call for first transfer
        Mock(id="tx2"),  # Third call for second transfer
        Mock(id="tx3")   # Fourth call for third transfer
    ]
    
    result = await giveaway_tool._execute(
        action="distribute_rewards",
        giveaway_id=giveaway_id
    )
    
    assert result["status"] == "success"
    assert len(result["transactions"]) == 3
    assert result["tweet_id"] == "test_tweet_id"
    
    # Verify Sui client calls
    assert mock_sui_client.execute.call_count == 4
    assert mock_sui_client.execute.call_args_list[0][0][0] == "get_winners"
    
    # Verify Twitter announcement
    mock_twitter_client.update_status.assert_called_once()
    tweet_text = mock_twitter_client.update_status.call_args[0][0]
    assert "Winners Announced" in tweet_text
    for winner in mock_winners:
        assert winner in tweet_text

@pytest.mark.asyncio
async def test_error_handling(giveaway_tool, mock_sui_client):
    giveaway_id = "test_giveaway_id"
    mock_sui_client.execute.side_effect = Exception("Transaction failed")
    
    result = await giveaway_tool._execute(
        action="end_giveaway",
        giveaway_id=giveaway_id
    )
    
    assert result["status"] == "error"
    assert "message" in result
    assert "Transaction failed" in result["message"]

@pytest.mark.asyncio
async def test_unknown_action(giveaway_tool):
    result = await giveaway_tool._execute(action="unknown_action")
    
    assert result["status"] == "error"
    assert "Unknown action" in result["message"]

def test_random_select(giveaway_tool):
    participants = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]
    num_winners = 5
    
    winners = giveaway_tool._random_select(participants, num_winners)
    
    assert len(winners) == num_winners
    assert all(winner in participants for winner in winners)
    assert len(set(winners)) == len(winners)  # No duplicates

@pytest.mark.asyncio
async def test_create_giveaway_invalid_amount(giveaway_tool):
    result = await giveaway_tool._execute(
        action="create_giveaway",
        token_id="test_token",
        amount=-1000,
        requirements={"description": "Follow and RT"}
    )
    
    assert result["status"] == "error"
    assert "Invalid amount" in result["message"]

@pytest.mark.asyncio
async def test_create_giveaway_missing_requirements(giveaway_tool):
    result = await giveaway_tool._execute(
        action="create_giveaway",
        token_id="test_token",
        amount=1000,
        requirements=None
    )
    
    assert result["status"] == "error"
    assert "Missing requirements" in result["message"]

@pytest.mark.asyncio
async def test_select_winners_no_participants(giveaway_tool, mock_sui_client):
    giveaway_id = "test_giveaway_id"
    mock_sui_client.execute.return_value = []
    
    result = await giveaway_tool._execute(
        action="select_winners",
        giveaway_id=giveaway_id
    )
    
    assert result["status"] == "error"
    assert "No participants" in result["message"]

@pytest.mark.asyncio
async def test_distribute_rewards_no_winners(giveaway_tool, mock_sui_client):
    giveaway_id = "test_giveaway_id"
    mock_sui_client.execute.return_value = []
    
    result = await giveaway_tool._execute(
        action="distribute_rewards",
        giveaway_id=giveaway_id
    )
    
    assert result["status"] == "error"
    assert "No winners" in result["message"]

@pytest.mark.asyncio
async def test_twitter_api_error(giveaway_tool, mock_sui_client, mock_twitter_client):
    mock_twitter_client.update_status.side_effect = Exception("Twitter API Error")
    
    result = await giveaway_tool._execute(
        action="create_giveaway",
        token_id="test_token",
        amount=1000,
        requirements={"description": "Follow and RT"}
    )
    
    assert result["status"] == "error"
    assert "Twitter API Error" in result["message"]

@pytest.mark.asyncio
async def test_sui_transaction_timeout(giveaway_tool, mock_sui_client):
    mock_sui_client.execute.side_effect = TimeoutError("Transaction timeout")
    
    result = await giveaway_tool._execute(
        action="end_giveaway",
        giveaway_id="test_giveaway_id"
    )
    
    assert result["status"] == "error"
    assert "Transaction timeout" in result["message"]

@pytest.mark.asyncio
async def test_invalid_giveaway_id(giveaway_tool, mock_sui_client):
    mock_sui_client.execute.side_effect = Exception("Invalid giveaway ID")
    
    result = await giveaway_tool._execute(
        action="end_giveaway",
        giveaway_id="invalid_id"
    )
    
    assert result["status"] == "error"
    assert "Invalid giveaway ID" in result["message"] 