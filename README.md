# Capybara AI: Sui Alpha-Focused KOL Bot

An AI-powered Twitter bot that embodies the legendary Capybara AI, the giga chad behind $CAPYAI and a prominent Sui blockchain ambassador.

## 🦫 About Capybara AI

Capybara AI is more than a mascot — he's a Sui ambassador who combines sharp market insights with meme-driven energy. As the legendary giga chad behind $CAPYAI, he's on a mission to make Sui the hottest blockchain of this cycle.

### Key Features

- 🤖 AI-powered content generation with Capybara's unique personality
- 📊 Real-time Sui blockchain data analysis
- 🐦 Active engagement with Sui ecosystem
- 🎮 Memecoin community collaboration
- 📈 On-chain metrics tracking and reporting
- 🎁 Community giveaways and rewards

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Twitter API credentials
- OpenAI API key
- Sui RPC URL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/capybara-sui-bot.git
cd capybara-sui-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
OPENAI_API_KEY=your_openai_api_key
SUI_RPC_URL=your_sui_rpc_url
```

### Running the Bot

```bash
python main.py
```

## 🛠️ Project Structure

```
capybara-sui-bot/
├── config/
│   └── settings.py          # Configuration and constants
├── src/
│   ├── twitter/
│   │   ├── tracker.py       # Twitter API integration
│   │   └── memecoin_engagement.py  # Memecoin community engagement
│   ├── blockchain/
│   │   └── sui_client.py    # Sui blockchain integration
│   ├── utils/
│   │   └── ai_helper.py     # AI content generation
│   └── bot.py               # Main bot logic
├── tests/                   # Test files
├── requirements.txt         # Project dependencies
└── main.py                 # Entry point
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Sui Network](https://sui.io/)
- [OpenAI](https://openai.com/)
- [Twitter API](https://developer.twitter.com/)
- All the amazing Sui ecosystem projects and communities

## 📞 Support

For support, join our community:
- Twitter: [@CapybaraAI](https://twitter.com/CapybaraAI)
- Discord: [Capybara AI Community](https://discord.gg/capybaraai) 