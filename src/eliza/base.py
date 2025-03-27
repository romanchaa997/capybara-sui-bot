from typing import List, Dict, Any, Callable, Awaitable, Union
from datetime import datetime
import asyncio

class Agent:
    def __init__(self, name: str, description: str, personality: str, tools: List[Any], memory: Any):
        self.name = name
        self.description = description
        self.personality = personality
        self.tools = tools
        self.memory = memory

    async def run(self):
        """Run the agent's main loop"""
        pass

class Tool:
    def __init__(self, name: str, description: str, function: Union[Callable, Awaitable]):
        self.name = name
        self.description = description
        self.function = function

    async def _execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute the tool's function"""
        if asyncio.iscoroutinefunction(self.function):
            return await self.function(action, **kwargs)
        return self.function(action, **kwargs)

class Memory:
    def __init__(self, short_term_window: int, long_term_window: int, max_entries: int):
        self.short_term_window = short_term_window
        self.long_term_window = long_term_window
        self.max_entries = max_entries
        self.entries = []

    def add(self, key: str, value: Any):
        self.entries.append((key, value, datetime.now()))
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)

    def get(self, key: str) -> Any:
        """Get the most recent value for a key"""
        for k, v, _ in reversed(self.entries):
            if k == key:
                return v
        return None

    def get_recent(self, key: str, n: int = 5) -> List[Any]:
        """Get the n most recent values for a key"""
        values = []
        for k, v, _ in reversed(self.entries):
            if k == key:
                values.append(v)
                if len(values) >= n:
                    break
        return values 