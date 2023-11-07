import aiohttp

import json
import bhaicord

from typing import (
    Optional,
    Dict,
    Any,
    List,
    Union,
    Tuple
)

__all__: Tuple[str] = ("HTTPClient", )


class Writer:
    def __init__(self):
        self.buffer = bytearray()

    async def write(self, data):
        self.buffer.extend(data)


class HTTPClient:

    """
    To make requests and authenticate
    """
    boundary = "boundary"

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = bhaicord.api_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def authenticate(self) -> None:
        """Creates the session"""

        # if self.session:
        # await self.session.close()

        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bot {self.bot_token}",
            "Accept": "application/json",
            "User-Agent": f"DiscordBot ({bhaicord.__github__}, {bhaicord.__version__})"}
        )

    @classmethod
    async def multipart_handler(
            cls,
            data: Union[str, Dict],
            files: List["bhaicord.File"]) -> "aiohttp.MultipartWriter":

        """Creates the multipart form-data

        Args:
            data (typing.Union[str, Dict]): The json payload
            files (List[cordic.File]): List of file objects
        Return:
            aiohttp.MultipartWriter

        """

        if isinstance(data, str):
            data = json.load(data)

        data["attachments"]: list = []
        writer = Writer()

        with aiohttp.MultipartWriter(boundary=cls.boundary) as mpwriter:

            for index, file in enumerate(files):
                data["attachments"].append(file.to_dict(index))

            mpwriter.append_json(data, headers={
                "Content-Disposition": "form-data; name=\"payload_json\"",
                "Content-Type": "application/json"
            })
            # loop through all files

            for index, file in enumerate(files):

                mpwriter.append(
                    file.content,
                    headers={
                        "Content-Disposition": f"form-data; name=\"files[{index}]\";"
                                               f" filename=\"{file.filename}\"",
                        "Content-Type": "application/text-plain"
                    }
                )

            await mpwriter.write(writer)
        return mpwriter

    @classmethod
    def request_handler(cls) -> Dict[str, Any]:
        """"""

    async def request(
            self, method: str,
            url: str,
            payload: Dict[str, Any] = None,
            files: Optional[List["bhaicord.File"]] = None

    ) -> Optional[aiohttp.ClientResponse]:

        """
        Custom request

        Arguments:
            method (str): HTTP valid method
            url (str): The endpoint
            payload (typing.Dict[str, Any]):
                A dict to send data (data or json) over the request

            files (typing.Optional[cordic.File]):
                A list of files

        Return: Optional[aiohttp.ClientResponse]

        As the documentation says, if we add a file to the request
        "application/json" must be replaced by "multipart/form-data"
        """
        # await self.authenticate()

        if not url.startswith("/"):
            url = f"/{url}"

        endpoint = self.api_url + url
        content_type = "application/json"

        if files:
            content_type = f'multipart/form-data; boundary="{self.boundary}"'
            kwargs = {'data': await HTTPClient.multipart_handler(payload, files)}
        else:
            kwargs = {'json': payload} if payload else {}
            # we avoid sending an empty dictionary which would cause an error

        rs = await self.session.request(
            method, endpoint, **kwargs,
            headers={
                "Content-Type": content_type
            }
        )
        # no content, we can't parse it to json
        if rs.status == 204:
            return

        if not rs.ok:
            # not done yet
            # cordic.errors.determine_error(code=rs.status)
            raise Exception('HTTP error')
        # print(rs.status)
        # await self.session.close()
        # for unknown reasons, closing this session gives an error lol
        return rs
