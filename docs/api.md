# API Documentation

## Tools API Reference

### BlockvisionTool

The BlockvisionTool provides market data and analytics for the Sui ecosystem.

#### Methods

##### get_market_data()
```python
async def get_market_data() -> Dict[str, Any]
```

Returns overall market data for the Sui ecosystem.

**Response:**
```json
{
    "status": "success",
    "market_data": {
        "total_market_cap": float,
        "24h_volume": float,
        "active_protocols": int,
        "total_value_locked": float,
        "market_trends": {
            "price": string,
            "volume": string
        }
    }
}
```

##### get_token_metrics(token_id: str)
```python
async def get_token_metrics(token_id: str) -> Dict[str, Any]
```

Returns detailed metrics for a specific token.

**Parameters:**
- `token_id`: The unique identifier of the token

**Response:**
```json
{
    "status": "success",
    "token_metrics": {
        "price": float,
        "market_cap": float,
        "volume_24h": float,
        "holders": int,
        "price_change_24h": float,
        "liquidity": float
    }
}
```

##### get_protocol_metrics(protocol: str)
```python
async def get_protocol_metrics(protocol: str) -> Dict[str, Any]
```

Returns metrics for a specific protocol.

**Parameters:**
- `protocol`: The name or identifier of the protocol

**Response:**
```json
{
    "status": "success",
    "protocol_metrics": {
        "tvl": float,
        "volume_24h": float,
        "users_24h": int,
        "fees_24h": float,
        "revenue_24h": float
    }
}
```

##### get_whale_activity()
```python
async def get_whale_activity() -> Dict[str, Any]
```

Returns recent whale activity on Sui.

**Response:**
```json
{
    "status": "success",
    "whale_activity": {
        "large_transactions": [
            {
                "amount": float,
                "timestamp": string
            }
        ],
        "whale_movements": [
            {
                "from": string,
                "to": string,
                "amount": float
            }
        ],
        "accumulation_trends": {
            "trend": string,
            "period": string
        }
    }
}
```

### GiveawayTool

The GiveawayTool manages token giveaways on the Sui blockchain.

#### Methods

##### create_giveaway(token_id: str, amount: int, requirements: Dict[str, Any])
```python
async def create_giveaway(
    token_id: str,
    amount: int,
    requirements: Dict[str, Any]
) -> Dict[str, Any]
```

Creates a new giveaway.

**Parameters:**
- `token_id`: The token to be given away
- `amount`: The amount of tokens to give away
- `requirements`: Dictionary containing giveaway requirements

**Response:**
```json
{
    "status": "success",
    "giveaway_id": string,
    "tweet_id": string
}
```

##### end_giveaway(giveaway_id: str)
```python
async def end_giveaway(giveaway_id: str) -> Dict[str, Any]
```

Ends an active giveaway.

**Parameters:**
- `giveaway_id`: The ID of the giveaway to end

**Response:**
```json
{
    "status": "success",
    "transaction_id": string,
    "message": string
}
```

##### select_winners(giveaway_id: str)
```python
async def select_winners(giveaway_id: str) -> Dict[str, Any]
```

Selects winners for a giveaway.

**Parameters:**
- `giveaway_id`: The ID of the giveaway

**Response:**
```json
{
    "status": "success",
    "winners": [string],
    "transaction_id": string
}
```

##### distribute_rewards(giveaway_id: str)
```python
async def distribute_rewards(giveaway_id: str) -> Dict[str, Any]
```

Distributes rewards to winners.

**Parameters:**
- `giveaway_id`: The ID of the giveaway

**Response:**
```json
{
    "status": "success",
    "transactions": [string],
    "tweet_id": string
}
```

### Error Responses

All methods may return the following error response:

```json
{
    "status": "error",
    "message": string
}
```

Common error messages:
- "API Error": External API call failed
- "Transaction failed": Blockchain transaction failed
- "Unknown action": Invalid action specified
- "Invalid parameters": Missing or invalid parameters

## Rate Limits

- Blockvision API: 100 requests per minute
- Sui RPC: 1000 requests per minute
- Twitter API: 300 requests per 3 minutes

## Best Practices

1. Always check the response status before processing data
2. Implement proper error handling
3. Cache frequently accessed data
4. Use appropriate timeouts for API calls
5. Monitor rate limits
6. Implement retry logic for failed requests
7. Keep private keys secure and never expose them in logs or responses 