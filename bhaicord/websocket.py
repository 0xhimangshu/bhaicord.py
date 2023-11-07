import typing

from aiohttp.client_ws import ClientWebSocketResponse, WSMsgType
import aiohttp

import bhaicord

import zlib
import attr
import json
import asyncio
import datetime

from typing import (
    Optional,
    Union
)

# Taken from discord Api documentation
# https://discord.com/developers/docs/topics/gateway#payload-compression
ZLIB_SUFFIX = b'\x00\x00\xff\xff'


__all__: typing.Tuple[str] = (
    "DiscordWebSocket",
    "Opcodes"
)

DictType = typing.Dict[str, typing.Any]


class Opcodes:
    """
    All opcodes
    """
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class DiscordWebSocket:
    """

    To connect to the gateaway and receive real-time events.

    Args:
        client (cordic.Client): The client is using this websocket
        intents (int): The intents discord provides
        heartbeat_interval (int): The interval in milliseconds
        sock: The socket
        sequence (int): for resuming sessions
        last_heartbeat: The last heartbeat done
        session_id: a value provided by discord
        has_disconnected (Optional[bool]): True if disconnected otherwise None


    """

    def __init__(self, client: bhaicord.Client, intents: int):

        self.client = client
        self.intents = intents

        self.gateaway_url = f"{bhaicord.gateaway_url}/?v=9&encoding=json&compress=zlib-stream"

        self.heartbeat_interval: Optional[int] = None
        self.sock: Optional[ClientWebSocketResponse] = None
        self.sequence: Optional[int] = None
        self.last_heartbeat: Optional[Union[int, datetime.datetime]] = None
        self.session_id: Optional[int] = None
        self.has_disconnected: Optional[bool] = None
        self.latency = None

    def identify(self) -> DictType:

        """Returns the identify"""

        return {
            "op": Opcodes.IDENTIFY,
            "d": {
                "token": self.client.bot_token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "bhaicord",
                    "$device": "bhaicord"
                },
                "presence": None
            }
        }

    @property
    def resume(self) -> DictType:
        """Returns the resume"""
        return {
            "op": Opcodes.RESUME,
            "d": {
                "token": self.client.bot_token,
                "session_id": self.session_id,
                "seq": self.sequence
            }
        }

    @staticmethod
    def _decompress(msg: WSMsgType.BINARY, inflator) -> Optional[str]:

        """Decompress a WSMsgType.BINARY value

        Args:
            msg (WSMsgType.BINARY): The data
        """

        # Algorithm taken in https://discord.com/developers/docs/topics/gateway#heartbeat

        buffer = bytearray()

        buffer.extend(msg)

        if msg[-4:] == ZLIB_SUFFIX:
            return inflator.decompress(buffer)

    async def __send_heartbeat(self) -> None:
        """Sends the heartbeat to the socket"""

        if not self.sock.closed:
            await self.sock.send_json(
                {
                    "op": Opcodes.HEARTBEAT,
                    "d": self.sequence
                }
            )

            self.last_heartbeat = datetime.datetime.now()

    async def __keep_socket_alive(self) -> None:
        """Sleeps a certain interval to send the heartbeat"""

        if self.heartbeat_interval:
            # await asyncio.sleep receives seconds to sleep, so we parse milliseconds to seconds
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await self.__send_heartbeat()

    async def __run_socket(self) -> None:
        """
        Starts receiving the data
        """
        inflator = zlib.decompressobj()

        while self.sock:

            task = asyncio.create_task(self.__keep_socket_alive())
            data = await self.sock.receive()

            if data.type == WSMsgType.CLOSE:
                await self.sock.close()

            elif data.type == WSMsgType.BINARY:

                payload = DiscordWebSocket._decompress(data.data, inflator=inflator)

                payload_json = json.loads(payload)

                event_data = payload_json["d"]
                self.sequence = payload_json.get("s")

                if payload_json["op"] == Opcodes.HELLO:
                    self.heartbeat_interval = event_data["heartbeat_interval"]
                    await self.sock.send_json(self.identify())

                elif payload_json["op"] == Opcodes.DISPATCH:
                    if payload_json["t"] == "READY":
                        self.session_id = event_data["session_id"]

                    await self.client.event_handler(payload_json["t"], event_data)

                elif payload_json["op"] == Opcodes.HEARTBEAT_ACK:
                    if self.heartbeat_interval is not None:
                        self.latency = (datetime.datetime.now() - self.last_heartbeat).total_seconds() * 1000

                elif payload_json["op"] == Opcodes.RECONNECT:
                    await self.sock.close()
                    self.has_disconnected = True

                    await self.start()

    async def start(self) -> None:
        """
        Make the session and starts running
        ``__run_socket`` function to start receiving data
        """
        async with aiohttp.ClientSession() as session:
            self.sock = await session.ws_connect(self.gateaway_url)

            if self.has_disconnected:
                await self.sock.send_json(self.resume)

            await self.__run_socket()