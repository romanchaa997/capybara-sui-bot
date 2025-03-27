"""
Eliza Framework for Capybara Sui Bot
"""

from .base import Agent, Tool, Memory
from .agents.capybara_agent import CapybaraAgent
from .tools.sui_tool import SuiTool
from .tools.blockvision_tool import BlockvisionTool
from .tools.giveaway_tool import GiveawayTool

__version__ = "0.1.0"
__author__ = "IgRomanych"

__all__ = [
    "Agent",
    "Tool",
    "Memory",
    "CapybaraAgent",
    "SuiTool",
    "BlockvisionTool",
    "GiveawayTool",
] 