from __future__ import annotations
import bhaicord
import asyncio
from typing import (
    Dict,
    Any,
    Callable,
    Optional,
    Union,
    List,
    TYPE_CHECKING
)
import inspect
from functools import wraps

import bhaicord


class Client:
    """
    My Client class where events will be called

    Args:
        intents (int): The intents for permissions
    """

    def __init__(self, intents: int, cache_size: int = 1500):
        self.intents: int = intents
        self.cache_size = int(cache_size)

        self.bot_token: str = "placeholder"

        self.ws = bhaicord.websocket.DiscordWebSocket(self, intents)
        self.http: bhaicord.HTTPClient = bhaicord.HTTPClient(bot_token="placeHolder")

        # storage
        self.events: Dict[str, Dict[str, Any]] = {}

        # cache
        self.user_cache: Dict[str, bhaicord.User.User] = {}
        self.message_cache: Dict[str, bhaicord.Message] = {}

        self._listeners: Dict[str, Dict[str, Any]] = {}
        self._message_create_listener = None

        self.loop = None

        # UNIMPLEMENTED
        self._storage = None

    @staticmethod
    def __add_on(event_or_listener: str) -> str:
        """adds on_ if needed"""
        if not event_or_listener.startswith("on_"):
            return f"on_{event_or_listener}"

        return event_or_listener

    @property
    def latency(self) -> Union[float, int]:
        """
        Returns the latency

        if latency is None, it'll return 0

        Return:
            typing.Union[float, int]
        """
        return self.ws.latency or 0

    def event(self, func: Callable[[Any], Any]) -> Callable:

        name = Client.__add_on(func.__name__)

        if not inspect.iscoroutinefunction(func):
            raise Exception("it has to be an async function")

        if name in self.events:
            raise Exception("There is already this event")

        self.events[name] = {"event": func, "listeners": []}

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    def listen(self, event_name: str) -> Callable:
        """Defining a listener

        Args:
            event_name (str): The event to listen

        """
        event_name = Client.__add_on(event_name)

        if event_name not in self.events:
            raise Exception("event not found")

        def wrapper(func: Callable[[Any], Any]):

            if not inspect.iscoroutinefunction(func):
                raise Exception("it has to be an async function")

            self.events[event_name]["listeners"].append(func)

            @wraps(func)
            async def call(*args, **kwargs):
                return await func(*args, **kwargs)
            return call
        return wrapper

    async def event_handler(self, event_name: str, event_data: Dict[str, Any]):

        """Checks for every event that happens to run"""

        async def call_event(fun: Callable[[Any], Any], **kwargs) -> None:

            if fun is None:
                return

            name = func_name

            obj = kwargs.get("data")

            task1 = asyncio.create_task(fun(obj))

            for listener in self.events.get(name)["listeners"]:
                task2 = asyncio.create_task(listener(obj))

        func_name = Client.__add_on(event_name.lower())

        if func_name not in self.events:
            return

        if event_name.lower() == "ready":

            ready_obj = bhaicord.ReadyEvent(data=event_data)
            f = self.events.get(func_name).get("event")

            await call_event(
                fun=f, data=ready_obj
            )

        if event_name.lower() == "message_create":

            message_obj = bhaicord.Message(data=event_data)
            if asyncio.isfuture(self._message_create_listener):
                try:
                    self._message_create_listener.set_result(message_obj)
                except asyncio.InvalidStateError:
                    pass

            f = self.events.get(func_name).get("event")

            await call_event(
                fun=f, data=message_obj
            )

    async def login_http(self) -> None:
        self.http.bot_token = self.bot_token

        await self.http.authenticate()
        await self.ws.start()

    def run(self, token: str) -> None:

        """Keeps the bot running

        Args:
            token (str): The token
        """
        self.bot_token = token

        bhaicord.CurrentClient.client = self

        self.loop = asyncio.get_event_loop()
        task = self.loop.create_task(self.login_http())
        try:
            self.loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()

            if self.ws and self.ws.sock:
                self.loop.run_until_complete(self.ws.sock.close())

    @staticmethod
    async def fetch_user(user_id: int) -> bhaicord.User:
        """Returns an user by id"""
        return await bhaicord.User.from_id(user_id)

    @staticmethod
    async def fetch_channel(channel_id: int) -> bhaicord.Channel:
        """Returns a channel by id"""
        return await bhaicord.Channel.from_id(channel_id)

    @staticmethod
    async def fetch_guild_roles(guild_id: int) -> List[bhaicord.Role]:
        """Returns a role by id"""
        return await bhaicord.Role.from_guild_id(guild_id)

    @staticmethod
    async def fetch_message(channel_id: int, message_id: int) -> bhaicord.Message:
        """Returns the Message by channel id and message id"""
        return await bhaicord.Message.from_id(
            channel_id=channel_id,
            message_id=message_id
        )

    @property
    async def connections(self) -> List["bhaicord.Connection"]:
        """
        A List of `Connection` objects
        """
        rs = await self.http.request(
            "GET",
            "/users/@me/connections"
        )

        return list(map(bhaicord.Connection, await rs.json()))

    @property
    async def user(self) -> bhaicord.User:
        """Gets the bot user"""

        rs = await self.http.request("GET", "/users/@me")
        return bhaicord.User(await rs.json())

    async def wait_for(
            self, event_name: Optional[str] = None,
            check: Optional[Union[Callable[[Any], Any], bool]] = None,
            timeout: Optional[float] = None

    ) -> Any:

        future = self.loop.create_future()
        self._message_create_listener = future

        # UNIMPLEMENTED
        if check is None:
            check = True

        return await asyncio.wait_for(future, timeout)
