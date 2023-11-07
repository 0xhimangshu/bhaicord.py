from __future__ import annotations
from typing import Optional, List, Dict, Any, TYPE_CHECKING

import bhaicord


from bhaicord.models.embed import Embed
from bhaicord.models.file import File

import aiohttp


async def async_send(
        *,
        content: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        file: Optional[File] = None,
        files: List[File] = None,
        allowed_mentions: Optional[Dict[str, Any]] = None,
        wait: bool = False,
        thread_id: Any = None,
        id_: Optional[int] = None,
        token: Optional[str] = None

) -> Optional["bhaicord.Message"]:

    if content is not None:
        content = str(content)

    if embed is not None and embeds is not None:
        raise Exception('Either embed or embeds')

    if file is not None and files is not None:
        raise Exception('Either file or files')

    if embeds is None:
        embeds = []

    if files is None:
        files = []

    if file is not None:
        files.append(file)

    if embed is not None:
        embeds.append(embed)

    if allowed_mentions is None:
        allowed_mentions = {}

    endpoint = f"/webhooks/{id_}/{token}"

    if wait is not None and isinstance(wait, bool):
        endpoint += "?wait=true"

    if thread_id is not None and isinstance(thread_id, (int, str)):
        endpoint += f"&thread_id={thread_id}"

    data = {
        "content": content,
        "username": username,
        "avatar_url": avatar_url,
        "tts": tts,
        "embeds": [em.to_dict() for em in embeds],
        "allowed_mentions": allowed_mentions
    }
    if files:
        content_type = f"multipart/form-data; boundary={bhaicord.HTTPClient.boundary}"
        kwargs = {"data": await bhaicord.HTTPClient.multipart_handler(data, files)}
    else:
        content_type = "application/json"
        kwargs = {"json": data}

    async with aiohttp.ClientSession() as session:
        rs = await session.request(
            "POST",
            f"{bhaicord.api_url}/{endpoint}",
            **kwargs,
            headers={
                "Content-Type": content_type
            }
        )
        if rs.status == 204:
            return

        return bhaicord.Message(await rs.json())


def sync_send() -> None:
    return


async def fetch_webhook_base() -> Optional["bhaicord.Webhook"]:
    return