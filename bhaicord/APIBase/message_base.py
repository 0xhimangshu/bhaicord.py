from __future__ import annotations

from typing import Union, Optional, Iterable, TYPE_CHECKING, Dict, Any, List
import bhaicord

from bhaicord.models.embed import Embed
from bhaicord.models.file import File

from bhaicord.models.message import Message


async def create_message(
        channel_id: Union[int, str],
        content: Optional[str] = None,
        tts: Optional[bool] = None,
        embeds: Optional[Iterable[Embed]] = None,
        embed: Optional[Embed] = None,
        file: Optional[File] = None,
        files: Optional[Iterable[File]] = None,
        allowed_mentions: Optional[Dict[str, bool]] = None) -> Message:
    client = bhaicord.CurrentClient.get_client()

    if allowed_mentions is None:
        allowed_mentions = {}

    if embeds is not None and embed is not None:
        raise Exception('Either embed or embeds')

    if files is not None and file is not None:
        raise Exception('Either file or files')

    if embeds is None:
        embeds = []

    if files is None:
        files = []

    if embed is not None:
        embeds.append(embed)

    if file is not None:
        files.append(file)

    if content is not None:
        # if the content is None, it won't send "None"
        content = str(content)

    rs = await client.http.request(
        "POST",
        f"/channels/{channel_id}/messages",
        payload={
            "content": content,
            "tts": tts,
            "embeds": [em.to_dict() for em in embeds],
            "allowed_mentions": allowed_mentions
        },
        files=files
    )

    return Message(await rs.json())


async def edit_message(
        channel_id: Optional[int] = None,
        message_id: Optional[int] = None,
        content: Optional[str] = None,
        embed: Optional[Embed] = None,
        embeds: Optional[Iterable[Embed]] = None,
        allowed_mentions: Optional[Dict[str, bool]] = None

) -> None:
    client = bhaicord.CurrentClient.get_client()

    if embed is not None and embeds is not None:
        raise Exception('Either embeds or embed')

    if embeds is None:
        embeds = []

    if embed is not None:
        embeds.append(embed)

    if content is not None:
        content = str(content)

    await client.http.request(
        "PATCH",
        f"channels/{channel_id}/messages/{message_id}",
        {
            "content": content,
            "embeds": [em.to_dict() for em in embeds],
            "allowed_mentions": allowed_mentions
        }
    )


async def delete_message(channel_id: int, message_id: int) -> None:
    client = bhaicord.CurrentClient.get_client()

    await client.http.request(
        "DELETE",
        f"channels/{channel_id}/messages/{message_id}"
    )


async def fetch_message_base(channel_id: int, message_id: int) -> Message:
    message_id = int(message_id)
    channel_id = int(channel_id)

    client = bhaicord.CurrentClient.get_client()

    msg = client.message_cache.get(message_id)

    if msg:
        return msg

    if len(client.message_cache) >= client.cache_size:
        key = list(client.message_cache.keys())

        del client.message_cache[key]

    rs = await client.http.request(
        "GET",
        f"channels/{channel_id}/messages/{message_id}"
    )
    message = Message(await rs.json())

    client.message_cache[message_id] = message

    return message
