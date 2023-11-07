from __future__ import annotations
import aiohttp
import bhaicord
from enum import Enum

from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union
)

from bhaicord.utils import DataType, make_optional
from bhaicord.models.user import User
from bhaicord.models.embed import Embed
from bhaicord.models.file import File

from bhaicord.APIBase.webhook_base import async_send


class WebhookTypes(Enum):
    incoming = 1
    channel_follower = 2
    application = 3

    def __str__(self) -> str:
        return self.name


class BaseWebhook:

    id: int
    type: WebhookTypes
    guild_id: Optional[int]
    channel_id: Optional[int]
    user: Optional[User]
    name: Optional[str]
    avatar: Optional[str]
    token: Optional[str]
    application_id: Optional[int]



    def __init__(self, url: str):
        self.url = url


        self.webhook_url: Optional[str] = None
        # This is just for a hint, that it also exists webhook_url,
        # but its only used when received from a data

    @classmethod
    def from_data(cls, webhook_data: DataType) -> BaseWebhook:
        """All Attributes of the webhook object"""

        base_webhook: BaseWebhook = super().__new__(cls)

        base_webhook.id = int(webhook_data["id"])
        base_webhook.type = WebhookTypes(webhook_data["type"])
        base_webhook.guild_id = make_optional(int, webhook_data.get("guild_id"))
        base_webhook.channel_id = make_optional(int, webhook_data.get("channel_id"))
        base_webhook.user = make_optional(User, webhook_data.get("user"))
        base_webhook.name = webhook_data.get("name")
        base_webhook.avatar = webhook_data.get("avatar")
        base_webhook.token = webhook_data.get("token")
        base_webhook.application_id = make_optional(int, webhook_data.get("application_id"))
        # NOT IMPLEMENTED
        base_webhook.source_guild = webhook_data.get("source_guild")
        base_webhook.source_channel = webhook_data.get("source_channel")
        base_webhook.webhook_url = webhook_data.get("url")

        return base_webhook



class Webhook(BaseWebhook):
    """Represents the Asynchronous Webhook object"""

    def __init__(self, *args, **kwargs):
        super(Webhook, self).__init__(*args, **kwargs)

        url = list(filter(lambda x: x, self.url.split("/")))

        try:
            self.token, self.id = url[::-1][0:2]
        except Exception:
            raise Exception('Does not seem to be a right url')

    @staticmethod
    async def from_id(id_: int) -> Webhook:
        """Fetches a webhook by id

        Args:
            id_ (int): The webhook id to fetch

        Return:
            Webhook: The webhook requested

        Note: Authentication is required
        """
        client = bhaicord.CurrentClient.get_client()

        rs = await client.http.request(
            "GET",
            f"/webhooks/{id_}"
        )

        return Webhook.from_data(await rs.json())

    @staticmethod
    async def from_token(webhook_id: int, token: str) -> Webhook:
        """Fetches a webhook by the webhook's token

        Args:
            webhook_id (int): The webhook id
            token (str): The webhook's token

        Return:
            Webhook: The webhook requested

        Note: Authentication not needed
        """

        async with aiohttp.ClientSession() as session:
            rs = await session.request(
                "GET",
                f"{bhaicord.api_url}/webhooks/{webhook_id}/{token}"
            )

        return Webhook.from_data(await rs.json())


    async def send(
            self,
            *,
            content: Optional[str] = None,
            username: Optional[str] = None,
            avatar_url: Optional[str] = None,
            tts: Optional[bool] = False,
            embed: Optional[Embed] = None,
            embeds: Optional[List[Embed]] = None,
            file: Optional[File] = None,
            files: Optional[List[File]] = None,
            allowed_mentions: Optional[DataType] = None,
            wait: bool = False,
            thread_id: Optional[Union[str, int]] = None

    ) -> Optional[bhaicord.Message]:

        """Execute the webhook"""

        msg = await async_send(
            content=content,
            username=username,
            avatar_url=avatar_url,
            tts=tts,
            embed=embed,
            embeds=embeds,
            file=file,
            files=files,
            allowed_mentions=allowed_mentions,
            wait=wait,
            thread_id=thread_id,
            id_=self.id,
            token=self.token
        )
        return msg


    @staticmethod
    async def create(channel_id: int, *, name: str, avatar: Optional[str] = None) -> Webhook:
        """Creates a webhook

        Args:
            channel_id (int): The channel id where this webhook will belong to
            name (str): The webhook's name
            avatar (typing.Optional[str]): The avatar, None by default

        Return:
            Webhook - The webhook created

        Note: Authentication required

        """

        client = bhaicord.CurrentClient.get_client()

        rs = await client.http.request(
            "POST",
            f"channels/{channel_id}/webhooks",
            {
                "name": name,
                "avatar": avatar
            }
        )
        return Webhook.from_data(await rs.json())



    async def edit(
            self,
            *,
            name: Optional[str] = None,
            avatar: Optional[str] = None,
            channel_id: Optional[int] = None) -> Optional[Webhook]:
        """
        Edits a webhook

        Args:
            name (str, Optional): The name
            avatar (str, Optional): The avatar
            channel_id (int, Optional): The channel id

        Note: Needs to be authenticated

        All following arguments can be null,
        they will all stay at their previous state
        """

        if not hasattr(self, "id"):
            return

        client = bhaicord.CurrentClient.get_client()


        rs = await client.http.request(
            "PATCH",
            f"/webhooks/{self.id}",
            {
                "name": name,
                "avatar": avatar,
                "channel_id": channel_id
            }
        )
        return Webhook.from_data(await rs.json())


    async def delete_by_id(self) -> None:
        """Deletes a webhook by id

        Note: needs to be authenticated
        """
        client = bhaicord.CurrentClient.get_client()

        await client.http.request(
            "DELETE",
            f"/webhooks/{self.id}"
        )

    async def delete_by_token(self) -> None:
        """Deletes a webhook by the token

        Note: Doesn't need to be authenticated
        """
        async with aiohttp.ClientSession() as session:
            await session.request("DELETE", f"{bhaicord.api_url}/webhooks/{self.id}/{self.token}")


    @staticmethod
    async def delete_message(
            *,
            webhook_id: Optional[int] = None,
            token: Optional[str] = None,
            message_id: Optional[int] = None,
            message: Optional[bhaicord.Message] = None,
            webhook: Optional[Webhook] = None,
            thread_id: Optional[int] = None
    ) -> None:
        """Deletes a webhook message
        Note: Authentication not required
        """
        thread_id = f"?thread_id={thread_id}" if thread_id else ""

        endpoint = bhaicord.api_url + "/webhooks/{}/{}/messages/{}{}"

        if not any([webhook_id, token, message_id]):
            if message is None or webhook is None:
                raise TypeError('message and webhook are needed')

            endpoint = endpoint.format(
                webhook.id,
                webhook.token,
                message.id,
                thread_id
            )
        else:
            endpoint = endpoint.format(
                webhook_id,
                token,
                message_id,
                thread_id
            )
        async with aiohttp.ClientSession() as session:
            await session.delete(url=endpoint)


    @staticmethod
    async def edit_message() -> bhaicord.Message:
        """Edits a message"""
