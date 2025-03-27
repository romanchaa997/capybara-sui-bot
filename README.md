# Capybara Sui Bot

A powerful AI agent built on ElizaOS for managing and engaging with the Sui blockchain ecosystem. The bot combines blockchain analytics, community engagement, and automated giveaways to create an interactive and informative experience for the Sui community.

## Features

### Blockchain Analytics
- Real-time market data tracking
- Token metrics and price analysis
- Protocol performance monitoring
- Whale activity tracking
- On-chain transaction analysis

### Community Engagement
- Automated Twitter interactions
- Sentiment analysis
- Community feedback collection
- Engagement metrics tracking
- Meme generation and sharing

### Giveaway Management
- Automated giveaway creation and management
- Smart winner selection
- On-chain reward distribution
- Twitter integration for announcements
- Engagement-based participant filtering

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/capybara-sui-bot.git
cd capybara-sui-bot
```

2. Install dependencies:
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `TWITTER_API_KEY`: Twitter API key
- `TWITTER_API_SECRET`: Twitter API secret
- `TWITTER_ACCESS_TOKEN`: Twitter access token
- `TWITTER_ACCESS_TOKEN_SECRET`: Twitter access token secret
- `OPENAI_API_KEY`: OpenAI API key
- `SUI_RPC_URL`: Sui blockchain RPC URL
- `BLOCKVISION_API_KEY`: Blockvision API key
- `SUI_WALLET_ADDRESS`: Sui wallet address for transactions
- `SUI_PRIVATE_KEY`: Sui wallet private key

## Usage

1. Start the bot:
```bash
python main.py
```

2. Run tests:
```bash
pytest tests/
```

3. Development mode:
```bash
python -m pytest tests/ -v
```

## Architecture

The bot is built on ElizaOS and consists of several key components:

### Core Components
- `CapybaraAgent`: Main agent class handling all operations
- `SuiTool`: Blockchain interaction and analytics
- `BlockvisionTool`: Market data and analytics
- `GiveawayTool`: Giveaway management
- `CommunityTool`: Community engagement

### Tools
Each tool is designed to handle specific functionality:

#### SuiTool
- Blockchain data retrieval
- Transaction monitoring
- Token price tracking
- Wallet integration

#### BlockvisionTool
- Market data analysis
- Protocol metrics
- Whale activity tracking
- Trend analysis

#### GiveawayTool
- Giveaway creation
- Winner selection
- Reward distribution
- Twitter integration

#### CommunityTool
- Twitter engagement
- Sentiment analysis
- Community feedback
- Content generation

## Testing

The project includes comprehensive tests for all components:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_blockvision_tool.py

# Run with coverage report
pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on [ElizaOS](https://github.com/elizaos/elizaos)
- Powered by [Sui Blockchain](https://sui.io)
- Analytics by [Blockvision](https://blockvision.org)

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 