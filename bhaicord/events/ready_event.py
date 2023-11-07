from typing import Dict, Any, List
import bhaicord


class ReadyEvent:

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.getaway_version: int = data["v"]
        self.user: "bhaicord.User" = bhaicord.User(data.get("user"))

        self.guilds: List[int] = [int(guild["id"]) for guild in data["guilds"]]

        self.session_id: str = data.get("session_id")
        self.shard: List[int] = data.get("shard", [])
        self.application = None