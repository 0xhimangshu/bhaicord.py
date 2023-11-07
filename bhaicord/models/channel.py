from __future__ import annotations

import datetime
from datetime import datetime
from typing import Optional, Dict, Any, Iterable, List, Union
import attr
import bhaicord
from bhaicord.models.message import Message
from bhaicord.models.embed import Embed
from bhaicord.models.file import File
from bhaicord.utils import simplify_attrs_from_dict, make_optional
from enum import Enum


class ChannelType(Enum):
    text = 0
    private = 1
    voice = 2
    group = 3
    category = 4
    guild_news = 5
    guild_news_thread = 10
    guild_public_thread = 11
    guild_private_thread = 12
    guild_stage_voice = 13
    guild_directory = 14
    guild_forum = 15

    def __str__(self) -> str:
        return self.name


class Channel:
    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.type: ChannelType = ChannelType(data["type"])
        self.guild_id: Optional[int] = make_optional(
            int,
            data.get("guild_id")
        )
        self.position: Optional[int] = data.get("position")
        self.permission_overwrites = data.get("permission_overwrites", [])
        self.name: Optional[str] = data.get("name")
        self.topic: Optional[str] = data.get("topic")
        self.nsfw: bool = data.get("nsfw", False)
        self.last_message_id: Optional[int] = make_optional(
            int,
            data.get("last_message_id")
        )
        self.bitrate: Optional[int] = data.get("bitrate")
        self.user_limit: Optional[int] = data.get("user_limit")
        self.rate_limit_per_user: Optional[int] = data.get("rate_limit_per_user")
        self.recipients: List[bhaicord.User.User] = list(map(bhaicord.User, data.get("recipients", [])))
        self.icon: Optional[str] = data.get("icon")
        self.owner_id: Optional[int] = make_optional(
            int,
            data.get("owner_id")
        )
        self.application_id: Optional[int] = make_optional(
            int,
            data.get("application_id")
        )
        self.parent_id: Optional[int] = make_optional(
            int,
            data.get("parent_id")
        )
        self.last_pin_timestamp: Optional[datetime] = make_optional(
            datetime.fromisoformat,
            data.get("last_pin_timestamp")
        )
        self.rtc_region: Optional[str] = data.get("rtc_region")

        self.video_quality_mode: Optional[int] = data.get("video_quality_mode")

        # -1 for default value when not found
        self.message_count: int = data.get("message_count", -1)
        self.member_count: int = data.get("member_count", -1)

        # Thread, UNIMPLEMENTED
        self.thread_metadata = data.get("thread_metadata")
        self.thread_member = data.get("thread_member")
        self.thread_default_auto_archive_duration: int = data.get("default_auto_archive_duration", -1)

        # PERMISSIONS UNIMPLEMENTED
        self.permissions = data.get("permissions")
        self.flags: int = data.get("flags", -1)

    async def send(
            self,
            content: Optional[str] = None,
            tts: Optional[bool] = None,
            embed: Optional[Embed] = None,
            embeds: List[Embed] = None,
            file: Optional[File] = None,
            files: Iterable[File] = None,
            allowed_mentions: Optional[Dict[str, bool]] = None

    ) -> Message:

        return await bhaicord.create_message(
            channel_id=self.id,
            content=content,
            tts=tts,
            embeds=embeds,
            embed=embed,
            files=files,
            file=file,
            allowed_mentions=allowed_mentions
        )

    @staticmethod
    async def from_id(channel_id: Union[int, str]) -> Channel:
        """Gets a channel by id"""

        return await bhaicord.fetch_channel_base(channel_id=channel_id)


@simplify_attrs_from_dict(
    ignore=["id", "guild_id", "type"]
)
class ChannelMention:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def channel_id(self) -> int:
        """Gets the id"""
        return int(self.data.get("id"))

    @property
    def guild_id(self) -> int:
        """Gets the guild id"""
        return int(self.data.get("guild_id"))

    @property
    def type(self) -> ChannelType:
        """Type of channel"""
        t = int(self.data.get("type"))
        return ChannelType(t)

    async def get_channel(self) -> Channel:
        """Gets this channel"""
        return await Channel.from_id(self.channel_id)