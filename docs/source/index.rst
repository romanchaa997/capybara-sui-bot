Welcome to Capybara Sui Bot's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :glob:

   installation
   usage
   api
   contributing
   changelog

English
-------

Capybara Sui Bot is an AI-powered Twitter bot that tracks and analyzes the Sui blockchain ecosystem. It provides real-time updates, community engagement, and automated giveaways.

Features:
- Real-time Sui ecosystem monitoring
- Automated content generation
- Community engagement tracking
- Automated giveaways
- Multi-language support

Русский
-------

Capybara Sui Bot - это бот с искусственным интеллектом для Twitter, который отслеживает и анализирует экосистему блокчейна Sui. Он предоставляет обновления в реальном времени, взаимодействие с сообществом и автоматизированные раздачи.

Возможности:
- Мониторинг экосистемы Sui в реальном времени
- Автоматическая генерация контента
- Отслеживание активности сообщества
- Автоматизированные раздачи
- Поддержка нескольких языков

中文
----

Capybara Sui Bot 是一个由人工智能驱动的 Twitter 机器人，用于跟踪和分析 Sui 区块链生态系统。它提供实时更新、社区互动和自动空投。

功能特点：
- Sui 生态系统实时监控
- 自动内容生成
- 社区互动跟踪
- 自动空投
- 多语言支持

Installation
-----------

1. First, let's install Rust. Please open a new PowerShell window as Administrator and run:
```powershell
winget install Rustlang.Rustup
```

2. Close and reopen your PowerShell window
3. Run this command to verify Rust is installed:
```powershell
rustc --version
```

4. Install the Python requirements:
```
pip install -r requirements.txt
python setup.py install
```

Quick Start
----------

.. code-block:: python

   from src.eliza.agents import CapybaraAgent
   
   # Initialize the agent
   agent = CapybaraAgent(config)
   
   # Run the bot
   await agent.run()

Contributing
-----------

We welcome contributions! Please see our :doc:`contributing` guide for details.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.  