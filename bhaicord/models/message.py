from __future__ import annotations
import attr
import asyncio
from datetime import datetime
from enum import Enum
from typing import (
    Union,
    BinaryIO,
    Optional,
    Dict,
    Any,
    TYPE_CHECKING,
    List,
    Iterable
)
from pydantic import BaseModel

import bhaicord

from bhaicord.models.embed import Embed
from bhaicord.models.file import File
from bhaicord.utils import DataType, make_optional
from bhaicord.APIBase.image_base import make_application_image


class MessageActivityTypes(Enum):
    join = 1
    spectate = 2
    listen = 3
    join_request = 5


class MessageTypes(Enum):
    default = 0
    recipient_add = 1
    recipient_remove = 2
    call = 3
    channel_name_change = 4
    channel_icon_change = 5
    channel_pinned_message = 6
    guild_member_join = 7
    user_premium_guild_subscription = 8
    user_premium_guild_subscription_tier_1 = 9
    user_premium_guild_subscription_tier_2 = 10
    user_premium_guild_subscription_tier_3 = 11
    channel_follow_add = 12
    guild_discovery_disqualified = 14
    guild_discovery_requalified = 15
    guild_discovery_grace_period_initial_warning = 16
    guild_discovery_grace_period_final_warning = 17
    thread_created = 18
    reply = 19
    chat_input_command = 20
    thread_starter_message = 21
    guild_invite_reminder = 22
    context_menu_command = 23


class StickerFormatType(Enum):
    png = 1
    apng = 2
    lottie = 3


class MessageActivityStructure:

    """Represents the Message Activity object"""

    def __init__(self, data: DataType):

        self.activity_type: Optional[MessageActivityTypes] = make_optional(
            MessageActivityTypes, data.get("activity_type")
        )

        self.party_id: Optional[int] = make_optional(
            int, data.get("party_id")
        )


class MessageReference(BaseModel):
    """Represents the Message Reference object"""

    message_id: Optional[int]
    """Id of the originating message"""

    channel_id: Optional[int]
    """Id of the originating message's channel"""

    guild_id: Optional[int]
    """Id of the originating message's guild"""

    fail_if_not_exists: Optional[bool]


class StickerItem:
    """Sticker Item object"""

    def __init__(self, sticker_item_data: DataType):
        self.id: Optional[int] = make_optional(
            int,
            sticker_item_data.get("id")
        )
        self.name: Optional[str] = sticker_item_data.get("name")

        self.format_type: StickerFormatType = make_optional(
            StickerFormatType,
            sticker_item_data.get("format_type")
        )

    def __repr__(self) -> str:
        return f"<StickerItem id={self.id} name={self.name!r} format_type={self.format_type}>"

    def __str__(self) -> str:
        return self.name


class InteractionType(Enum):
    ping = 1
    application_command = 2
    message_component = 3
    application_command_autocomplete = 4
    modal_submit = 5


class MessageInteraction:
    def __init__(self, data: DataType):
        self.id: Optional[int] = make_optional(int, data.get("id"))

        self.type: Optional[InteractionType] = make_optional(
            InteractionType,
            data.get("type")
        )
        self.name: Optional[str] = data.get("name")

        self.user: Optional[bhaicord.User.User] = make_optional(
            bhaicord.User.User,
            data.get("user")
        )


class Application:
    def __init__(self, data: DataType):
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.icon: Optional[str] = data.get("icon")
        self.description: str = data["description"]
        self.rpc_origins: List[str] = data.get("rpc_origins", [])
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]
        self.terms_of_service_url: Optional[str] = data.get("terms_of_service_url")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy_url")
        self.owner = bhaicord.utils.make_optional(
            bhaicord.User,
            data.get("owner", {})
        )
        self.guild_id: Optional[str] = data.get("guild_id")
        self.primary_sku_id: Optional[str] = data.get("primary_sku_id")
        self.slug: Optional[str] = data.get("slug")
        self.cover_image: Optional[str] = data.get("cover_image")
        self.flags: Optional[int] = data.get("flags")
        self.tags: List[str] = data.get("tags", [])

    @property
    def icon_url(self) -> Optional[str]:
        """The icon url"""
        return make_application_image(self.id, self.icon)

    @property
    def cover_url(self) -> Optional[str]:
        """Cover url"""
        return make_application_image(self.id, self.cover_image)


# @cordic.utils.simplify_attrs_from_dict(ignore=["id"])
class Message:

    """
    Message Object

    """

    def __init__(self, data: Dict[str, Any]):

        self.id: int = int(data["id"])
        self.channel_id: int = int(data["channel_id"])
        self.guild_id: Optional[str] = data.get("guild_id")

        if self.guild_id is not None:
            self.guild_id = int(self.guild_id)

        self.member: bhaicord.Member = bhaicord.make_optional(bhaicord.Member, data.get("member"))
        self.author: bhaicord.User = bhaicord.User(
            data["author"],
            member_data=data.get("member")
        )
        self.content: str = data["content"]
        self.timestamp: datetime = datetime.fromisoformat(data["timestamp"])

        self.edited_timestamp: Optional[datetime] = bhaicord.make_optional(
            datetime.fromisoformat, data.get("edited_timestamp")
        )
        self.tts: bool = data["tts"]

        self.mention_everyone: bool = data["mention_everyone"]
        self.mentions: List[bhaicord.User.User] = list(map(bhaicord.User, data.get("mentions", [])))
        self.mention_roles: List[int] = [int(id_) for id_ in data["mention_roles"]]

        self.mention_channels: List[bhaicord.ChannelMention] = list(map(
            bhaicord.ChannelMention,
            data.get("mention_channels", [])
        ))
        self.attachments: List[bhaicord.Attachment] = list(map(
            bhaicord.Attachment,
            data.get("attachments", [])
        ))
        self.embeds: List[bhaicord.Embed] = list(map(
            bhaicord.Embed.from_dict,
            data.get("embeds", [])
        ))
        self.reactions: List[bhaicord.Reaction] = list(map(
            bhaicord.Reaction,
            data.get("reactions", [])
        ))

        self.nonce: Optional[Union[int, str]] = data.get("nonce")
        self.pinned: bool = data.get("pinned")
        self.webhook_id: Optional[str] = data.get("webhook_id")
        self.type: int = MessageTypes(data["type"])

        self.activity: Optional[MessageActivityStructure] = MessageActivityStructure(data.get("activity", {}))

        self.application: Optional[Application] = bhaicord.make_optional(
            Application,
            data.get("application")
        )
        self.app = self.application
        self.application_id: Optional[int] = data.get("application_id")

        self.message_reference: MessageReference = MessageReference(
            **data.get("message_reference", {}))

        self.referenced_message: Message = make_optional(
            Message,
            data.get("referenced_message")
        )
        self.flags: Optional[int] = data.get("flags")

        self.interaction: Optional[MessageInteraction] = make_optional(
            MessageInteraction,
            data.get("interaction")
        )

        self.thread = data.get("thread", {})
        self.components = data.get("components", [])
        self.sticker_items = list(map(StickerItem, data.get("sticker_items", [])))

    @staticmethod
    async def from_id(channel_id: int, message_id: int) -> Message:
        """Returns the message by channel id and message id"""
        return await bhaicord.fetch_message_base(channel_id=channel_id, message_id=message_id)

    async def send(
            self,
            content: Optional[str] = None,
            tts: Optional[bool] = None,
            embed: Optional[Embed] = None,
            embeds: List[Embed] = None,
            file: Optional[File] = None,
            files: Iterable[File] = None,
            allowed_mentions: Optional[Dict[str, bool]] = None, *,
            channel_id: Optional[int] = None,
            delete_after: Optional[float] = None

    ) -> Message:

        message_object = await bhaicord.create_message(
            channel_id=channel_id or self.channel_id,
            content=content,
            tts=tts,
            embeds=embeds,
            embed=embed,
            files=files,
            file=file,
            allowed_mentions=allowed_mentions
        )

        if delete_after is not None:
            await message_object.delete(delay=delete_after)

        return message_object

    async def delete(self, *, delay: Optional[float] = None) -> None:
        """Deletes this message

        Keyword args:
            delay (typing.Optional[float]): the delay before deleting
        """
        if delay is not None:

            async def delete(delay_: float):

                await asyncio.sleep(delay_)
                await bhaicord.delete_message(self.channel_id, self.id)

            asyncio.create_task(delete(delay))
        else:
            await bhaicord.delete_message(self.channel_id, self.id)

    async def edit(
            self, *,
            channel_id: Optional[int] = None,
            message_id: Optional[int] = None,
            content: Optional[str] = None,
            embed: Optional[Embed] = None,
            embeds: Optional[Iterable[Embed]] = None,
            allowed_mentions: Optional[Dict[str, bool]] = None

    ) -> None:

        """Edits a message"""

        if channel_id is None:
            channel_id = self.channel_id

        if message_id is None:
            message_id = self.id

        await bhaicord.edit_message(
            channel_id=channel_id,
            message_id=message_id,
            content=content,
            embed=embed,
            embeds=embeds,
            allowed_mentions=allowed_mentions
        )

    async def pin(self, *,
                  channel_id: Optional[int] = None,
                  message_id: Optional[int] = None) -> None:
        """Pins a message"""

        client = bhaicord.CurrentClient.get_client()

        if not client:
            raise bhaicord.ClientNotFound

        if channel_id is None:
            channel_id = self.channel_id

        if message_id is None:
            message_id = self.id

        await client.http.request(
            "PUT",
            f"/channels/{channel_id}/pins/{message_id}"
        )

    async def unpin(self, *,
                    channel_id: Optional[int] = None,
                    message_id: Optional[int] = None) -> None:
        """Unpins a message"""

        client = bhaicord.CurrentClient.get_client()

        if not client:
            raise bhaicord.ClientNotFound

        if channel_id is None:
            channel_id = self.channel_id

        if message_id is None:
            message_id = self.id

        await client.http.request(
            "DELETE",
            f"/channels/{channel_id}/pins/{message_id}"
        )

    async def crosspost(
            self,
            channel_id: Optional[int] = None,
            message_id: Optional[int] = None) -> Message:

        channel_id = channel_id or self.channel_id
        message_id = message_id or self.id

        client = bhaicord.CurrentClient.get_client()

        rs = await client.http.request(
            "POST",
            f"/channels/{channel_id}/messages/{message_id}/crosspost")

        return Message(await rs.json())

    async def bulk_delete(
            self,
            message_ids: Iterable[int],
            channel_id: Optional[int] = None,
            guild_id: Optional[int] = None) -> None:

        """Bulk delete messages from 2 to 100

        Args:
            channel_id (typing.Optional[int]): the channel id.
                if it's None, it will take the channel id from this instance

            message_ids (typing.Iterable[int]): All message ids to delete

            guild_id (typing.Optional[int]): Guild id.
                if it's None, it will take the guild id from this instance

        Note:
            Messages older than 2 weeks will not be deleted
        """
        # if it's an empty list
        if not message_ids:
            return

        # avoids repetitive message ids, which will return 404 response
        message_ids = list(set(message_ids))

        channel_id = channel_id or self.channel_id
        guild_id = guild_id or self.guild_id

        client = bhaicord.CurrentClient.get_client()

        await client.http.request(
            "POST",
            f"/channels/{channel_id}/messages/bulk-delete",
            {
                "guild_id": guild_id,
                "messages": list(message_ids)
            }
        )