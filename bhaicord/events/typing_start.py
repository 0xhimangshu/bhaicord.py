from typing import (
    Union,
    Optional,
    Dict,
    Any
)
import datetime
import bhaicord

from bhaicord.utils import make_optional
from bhaicord.models.guild import Member


class TypingStartEvent:
    """Typing start event"""

    def __init__(self, data: Dict[str, Any]):
        self.channel_id: str = data.get("channel_id")

        if self.channel_id is not None:
            self.channel_id = int(self.channel_id)

        self.guild_id: str = data.get("guild_id")

        if self.guild_id is not None:
            self.guild_id = int(self.guild_id)

        self.user_id: str = data.get("user_id")

        if self.user_id is not None:
            self.user_id = int(self.user_id)

        self.timestamp = datetime.datetime.fromtimestamp(data.get("timestamp"))
        self.member = make_optional(Member, data.get("member"))