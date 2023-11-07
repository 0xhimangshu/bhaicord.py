from typing import (
    TYPE_CHECKING,
    Optional,
    List
)

from bhaicord.utils import (
    Utilities,
    _T,
    T,
    DataType,
    make_optional
)
from bhaicord.models.user import User
from bhaicord.models.role import Role
import bhaicord


class Emoji:
    """Represents the emoji Object"""

    def __init__(self, data: DataType):
        self.id: Optional[str] = data.get("id")

        if self.id:
            self.id = int(self.id)

        self.name: Optional[str] = data.get("name")

        self.roles: List[Role] = [Role(d) for d in data.get("roles", [])]
        self.user: Optional[User] = make_optional(
            User,
            data.get("user")
        )
        self.require_colons: bool = data.get("require_colons", False)
        self.managed: bool = data.get("managed", False)
        self.animated: bool = data.get("animated", False)
        self.available: bool = data.get("available", True)

    def __str__(self) -> str:
        if self.animated:
            return f'<a:{self.name}:{self.id}>'
        return f'<:{self.name}:{self.id}>'

    def __repr__(self) -> str:
        return f"<Emoji id={self.id} name={self.name!r} animated={self.animated}>"

    @property
    def url(self) -> str:
        """The url of this emoji"""
        fmt = 'gif' if self.animated else 'png'
        return f'{bhaicord.cdn_url}/emojis/{self.id}.{fmt}'


class Reaction:
    """Represents a reaction Object"""

    def __init__(self, reaction_data: DataType):
        self.count: int = reaction_data.get("count", 1)
        self.emoji: Optional[Emoji] = make_optional(Emoji, reaction_data.get("emoji"))
        self.me: Optional[bool] = reaction_data.get("me")

    def __repr__(self) -> str:
        return f"<Reaction emoji={str(self.emoji)} " \
               f"count={self.count} " \
               f"me={self.me}>"