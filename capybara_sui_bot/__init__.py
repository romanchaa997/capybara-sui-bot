"""
Capybara Sui Bot - A Sui ecosystem-focused AI bot.
"""

__version__ = "0.1.0"
__author__ = "IgRomanych"

from .bot import CapybaraBot
from .monitors import DeFiMonitor, PriceMonitor, CommunityManager

__all__ = ["CapybaraBot", "DeFiMonitor", "PriceMonitor", "CommunityManager"] 