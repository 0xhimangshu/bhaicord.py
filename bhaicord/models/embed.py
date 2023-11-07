from __future__ import annotations

from typing import (
    Optional,
    Dict,
    Any,
    List,
    Callable,
    Iterable
)
from typing_extensions import Literal

from bhaicord.utils import from_obj_to_dict, is_object, make_optional, DataType
import attr
import inspect

DictType = Dict[str, Any]

# The embed types
EmbedTypes = Literal[
    'rich',
    'image',
    'video',
    'gifv',
    'article',
    'link'
]


@attr.define(kw_only=True)
class EmbedFooter:
    """Represents an EmbedFooter object"""

    text: str
    """Footer text"""

    icon_url: Optional[str] = attr.field(default=None)
    """The icon url"""

    proxy_icon_url: Optional[str] = attr.field(default=None)
    """A proxied url for the footer icon"""


@attr.define(kw_only=True)
class EmbedImage:
    """Represents the embed image"""

    url: str
    """The image url"""

    proxy_url: Optional[str] = attr.field(default=None)
    """The proxied url for the embed image"""

    height: Optional[int] = attr.field(default=None)
    """The height of the image"""

    width: Optional[int] = attr.field(default=None)
    """The width of the image"""


@attr.define(kw_only=True)
class EmbedVideo:
    """Embed video"""

    url: str
    """The url"""

    proxy_url: Optional[str] = attr.field(default=None)
    """A proxied url"""

    height: Optional[int] = attr.field(default=None)
    """The height of the embed video"""

    width: Optional[int] = attr.field(default=None)
    """The width of the embed video"""


@attr.define(kw_only=True)
class EmbedThumbnail:
    """Embed Thumbnail"""

    url: str
    """source url of thumbnail"""

    proxy_url: Optional[str] = attr.field(default=None)
    """A proxied url of the thumbnail"""

    height: Optional[int] = attr.field(default=None)
    """Height of thumbnail image"""

    width: Optional[int] = attr.field(default=None)
    """Width of the thumbnail image"""


@attr.define(kw_only=True)
class EmbedField:
    """An Embed Field"""

    name: str = attr.field(repr=True)
    """The name"""

    value: str = attr.field(repr=True)
    """The value"""

    inline: bool = attr.field(repr=True)
    """The inline for a new row"""


@attr.define(kw_only=True)
class EmbedProvider:
    """Embed Provider"""

    name: Optional[str] = attr.field(default=None, repr=True)
    """The name"""

    url: Optional[str] = attr.field(default=None, repr=True)
    """The url"""


@attr.define
class EmbedAuthor:

    """Embed Author object"""

    name: str = attr.field(repr=True)
    """The author's name"""

    url: Optional[str] = attr.field(default=None)
    """The author url"""

    icon_url: Optional[str] = attr.field(default=None)
    """Url of the user icon"""

    proxy_icon_url: Optional[str] = attr.field(default=None)
    """A proxied url of the user icon"""


class Embed:
    """Embed Builder"""

    def __init__(
            self,
            title: Optional[str] = None,
            *,
            description: Optional[str] = None,
            color: Optional[int] = None,
            colour: Optional[int] = None,
            url: Optional[str] = None,
            timestamp: Optional[str] = None
    ) -> None:

        self.title = title
        self.description = description

        if color is not None and colour is not None:
            raise Exception("Either color or colour")

        if color is None:
            color = colour

        self.color = color
        self.url = url
        self.timestamp = timestamp

        self._fields: List[DictType] = []

        self._thumbnail = {}
        self._image = {}
        self._video = {}
        self._provider = {}
        self._author = {}
        self._footer = {}
        self.type: Optional[EmbedTypes] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Embed:
        """From dict to object"""

        embed: Embed = super().__new__(cls)
        # creates an embed object without calling __init__, YOU SHOULD NEVER CALL THIS

        embed.title = data.get("title")
        embed.description = data.get("description")
        embed.color = data.get("color")
        embed.colour = data.get("color")
        embed.url = data.get("url")
        embed.timestamp = data.get("timestamp")
        embed._thumbnail = make_optional(EmbedThumbnail, kwargs=data.get("thumbnail", {}))
        embed._image = make_optional(EmbedImage, kwargs=data.get("image", {}))
        embed._video = make_optional(EmbedVideo, kwargs=data.get("video", {}))
        embed._provider = make_optional(EmbedProvider, kwargs=data.get("provider"))
        embed._author = make_optional(EmbedAuthor, kwargs=data.get("author"))
        embed._footer = make_optional(EmbedAuthor, kwargs=data.get("footer"))
        embed.type = data.get("type")
        embed._fields = []

        for field in data.get("fields", []):
            embed._fields.append(EmbedField(**field))

        return embed

    @property
    def footer(self) -> DictType:
        """Gets the footer"""
        return self._footer

    @property
    def fields(self) -> List[DictType]:
        """Gets the fields"""
        return self._fields

    @property
    def thumbnail(self) -> DictType:
        """Gets the thumbnail"""
        return self._thumbnail

    @property
    def image(self) -> DictType:
        """Gets the image"""
        return self._image

    @property
    def video(self) -> DictType:
        """Gets the video object"""
        return self._video

    @property
    def provider(self) -> DictType:
        """Gets the provider object"""
        return self._provider

    @property
    def author(self) -> DictType:
        """Gets the author object"""
        return self._author

    def set_provider(self, name: Optional[str] = None, url: Optional[str] = None) -> Embed:
        """
        Sets the embed provider

        Args:
            name (typing.Optional[str]):
                name of the provider

            url (typing.Optional[str]):
                url of provider
        """
        self._provider = EmbedProvider(name=name, url=url)
        return self

    def set_image(self,
                  url: str,
                  proxy_url: Optional[str] = None,
                  height: Optional[int] = None,
                  width: Optional[int] = None) -> Embed:

        """Sets an image to the embed

        Args:
            url (str)
            proxy_url (typing.Optional[str])
            height (typing.Optional[int])
            width (typing.Optional[int])

        """
        self._image = EmbedImage(
            url=url,
            proxy_url=proxy_url,
            height=height,
            width=width
        )
        return self

    def set_footer(self,
                   text: str,
                   icon_url: Optional[str] = None,
                   proxy_icon_url: Optional[str] = None) -> Embed:

        """Sets a footer to the embed object

        Arguments:
            text (str): The footer text
            icon_url (str): The icon url
            proxy_icon_url (str): The proxied url for the icon

        """

        self._footer = EmbedFooter(
            text=str(text),
            icon_url=icon_url,
            proxy_icon_url=proxy_icon_url
        )

        return self

    def set_thumbnail(self,
                      url: str,
                      proxy_url: Optional[str] = None,
                      height: Optional[int] = None,
                      width: Optional[int] = None) -> Embed:
        """
        Sets a thumbnail to the embed object

        Args:
            url (str): The url for the image
            proxy_url (typing.Optional[str]): the proxy url
            height (typing.Optional[int]): the height of the image
            width (typing.Optional[int]): the width of the image
        """

        self._thumbnail = EmbedThumbnail(
            url=str(url),
            proxy_url=proxy_url,
            height=height,
            width=width
        )

        return self

    def set_author(self,
                   name: str,
                   url: Optional[str] = None,
                   icon_url: Optional[str] = None,
                   proxy_icon_url: Optional[str] = None) -> Embed:

        """
        Sets an author to the embed object

        Args:
            name (str): author's name
            url (typing.Optional[str]): The url
            icon_url (typing.Optional[str]): The icon url
            proxy_icon_url (typing.Optional[str]): a proxied icon url
        """

        self._author = EmbedAuthor(
            name=str(name),
            url=url,
            icon_url=icon_url,
            proxy_icon_url=proxy_icon_url)

        return self

    def add_field(
            self,
            name: str,
            value: str,
            inline: bool = False
    ) -> Embed:

        """
        Add a new field to the Embed object

        Args:
            name (str): The name of the field
            value (str): The value
            inline (bool): Whether to be or not in a new row

        """
        self._fields.append(
            EmbedField(name=str(name), value=str(value), inline=bool(inline))
        )
        return self

    def delete_field(self, index: int) -> Embed:
        """Deleted an Embed field from the index given"""
        try:
            self._fields.pop(index)
        except IndexError:
            ...
        return self

    def edit_field(self, index: int, name: str, value: str, inline: bool = False) -> Optional[Embed]:
        """Edits an Embed Field from the index given

        Args:
            index (int): The index of our embed field
            name (str): The new name
            value (str): The new value
            inline (bool): The new inline value
        """

        field = EmbedField(name=name, value=value, inline=inline)
        try:
            self._fields[index] = field
        except IndexError:
            return

        return self

    def to_dict(self) -> DictType:
        """The embed object into a dictionary"""

        args = {}
        for key, value in self.__dict__.items():

            if key.startswith("_"):
                key = key.strip("_")

            if isinstance(value, list):

                args[key] = []

                for field in value:
                    if is_object(field):
                        args[key].append(from_obj_to_dict(field))

            elif is_object(value):
                args[key] = from_obj_to_dict(value)

            else:
                args[key] = value
        return args