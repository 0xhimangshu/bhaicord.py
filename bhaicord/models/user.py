from __future__ import annotations

from typing import (
    Optional,
    Dict,
    Any,
    final,
    List,
    Union,
    Tuple,
    TYPE_CHECKING
)

import enum
import datetime
import bhaicord

__all__: Tuple[str] = (
    "UserFlag",
    "User",
    "ConnectionVisibility",
    "Connection",
    "PremiumTypes"
)

T = List[Dict[str, Any]]


@final
class UserFlag(enum.Flag):

    NONE = 0
    DISCORD_EMPLOYEE = 1 << 0
    PARTNERED_SERVER_OWNER = 1 << 1
    HYPESQUAD_EVENTS = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_BRAVERY = 1 << 6
    HYPESQUAD_BRILLIANCE = 1 << 7
    HYPESQUAD_BALANCE = 1 << 8
    EARLY_SUPPORTER = 1 << 9
    TEAM_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    EARLY_VERIFIED_DEVELOPER = 1 << 17
    DISCORD_CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19


class User:
    """Represents a discord user

    Attributes:
        id (str): Hello world

    """

    def __init__(self, data: Dict[str, Any], member_data: Optional[Dict[str, Any]] = None):

        self.member_data = member_data

        if self.member_data is None:
            self.member_data = {}

        self.avatar_size: int = 4096
        self.banner_size: int = 4096

        self.id = int(data["id"])
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar_hash: str = data["avatar"]
        self.bot: Optional[bool] = data.get("bot", False)
        self.system: Optional[bool] = data.get("system")
        self.mfa_enabled: Optional[bool] = data.get("mfa_enabled")
        self.banner_hash: Optional[str] = data.get("banner")
        self.accent_color: Optional[int] = data.get("accent_color")
        self.locale: Optional[str] = data.get("locale")
        self.verified: Optional[bool] = data.get("verified")
        self.email: Optional[str] = data.get("email")
        self.flags: Optional[int] = data.get("flags")

        self.premium_type: Optional[PremiumTypes] = bhaicord.utils.make_optional(PremiumTypes, data.get("premium_type"))

        self.public_flags: Optional[int] = data.get("public_flags")

    def __str__(self) -> str:
        return f"{self.username}#{self.discriminator}"

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' bot={self.bot}"

    def __eq__(self, other: 'User') -> bool:
        return self.id == other.id

    @property
    def mention(self) -> str:
        """
        Return a discord mention

        Example:
            print(some_user.mention)\n
            # <@some_user.id>

        Return:
            str
        """
        return f"<@{self.id}>"

    def set_avatar_size(self, size: int) -> None:
        """Helper method to set the avatar size

        Args:
            size (int): The size for the avatar.
        """
        self.avatar_size = size

    def set_banner_size(self, size: int) -> None:
        """Helper method to set the banner size

        Args:
            size (int): The size for the banner.
        """
        self.banner_size = size

    def _make_image(self, hash_: Optional[str] = None, avatar: bool = True) -> Optional[str]:
        """Builds the avatar url

        Args:

            avatar (bool, Optional):
                True for avatar's url, False for banner's.

        Note:
            ``avatar`` is True by default
        """
        if avatar:
            size = self.avatar_size
        else:
            size = self.banner_size

        return bhaicord.make_image_url(
            user_id=self.id,
            hash_=hash_,
            size=size,
            avatar=avatar,
            tag=int(self.discriminator)
        )

    @property
    def avatar_url(self) -> Optional[str]:
        """Gets the user's avatar url

        if avatar hash is None, returns None

        Return:
            typing.Optional[str]:
                default avatar, custom avatar or None
        """
        return self._make_image(
            hash_=self.avatar_hash
        )

    @property
    def default_avatar_url(self) -> str:
        """Gets the user's default profile"""
        return self._make_image()

    @property
    def banner_url(self) -> Optional[str]:
        """Gets the user's avatar url

        if banner hash is None, returns None

        Return:
            (typing.Optional[str]):
                The banner url, it might be None
        """

        return self._make_image(hash_=self.banner_hash, avatar=False)

    def banner_color(self, into_hex: bool = False) -> Optional[Union[int, str]]:

        """
        Gets the banner color of an user

        Args:
            into_hex (bool, Optional):
                True if we want to return the hex in string,
                False for the digit only.
                It's False by default

        Returns:
            typing.Union[str, int]
                the digit or hex in string
        """
        if self.accent_color is None:
            return

        if not isinstance(into_hex, bool):
            into_hex = bool(into_hex)

        if into_hex:
            return str(hex(int(self.accent_color)))

        return int(self.accent_color)

    @property
    def is_premium(self) -> bool:
        """
        Checks if the user is premium (Nitro)

        Return: bool
        """
        return self.premium_type in (
            PremiumTypes.NITRO_CLASSIC.value,
            PremiumTypes.NITRO.value
        )

    @property
    def display_name(self) -> str:
        """Display the nickname if possible, otherwise the username"""
        return self.member_data.get("nick") or self.username

    @property
    def created_on(self) -> datetime.datetime:
        """The date and time this user was created"""
        return bhaicord.utils.snowflake_to_date(self.id)

    @classmethod
    async def from_id(cls, user_id: int) -> User:
        """Fetches the user by the id"""
        return await bhaicord.fetch_user_base(user_id=user_id)


class Connection:

    def __init__(self, data: Dict[str, Any]):

        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: str = data["type"]
        self.revoked: Optional[bool] = data.get("revoked")
        self.integrations: Optional[T] = data.get("integrations")
        self.verified: bool = data["verified"]
        self.friend_sync: bool = data["friend_sync"]
        self.show_activity: bool = data["show_activity"]

        self.visibility: Optional[ConnectionVisibility] = bhaicord.utils.make_optional(
            ConnectionVisibility, data["visibility"]
        )


@final
class ConnectionVisibility(enum.Enum):

    NONE = 0
    EVERYONE = 1


@final
class PremiumTypes(enum.Enum):

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2