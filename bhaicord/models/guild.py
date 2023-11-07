from typing import (
    List,
    Optional,
    Dict,
    Any,
    Tuple,
    Union,
    TYPE_CHECKING

)

import datetime
from datetime import datetime

from bhaicord.models.user import User
from bhaicord.utils import make_optional

# __all__: Tuple[str] = (
# "Member",
# "PartialGuild",
# "Guild"
# )


T = Dict[str, Any]


class Member:
    def __init__(self, data: T):
        self._user: User = make_optional(
            User,
            data.get("user")
        )

        self.nick: Optional[str] = data.get("nick")
        self.guild_avatar_hash: Optional[str] = data.get("avatar")
        self.role_ids: List[Any] = data.get("roles", [])

        if data.get("premium_since"):
            self.premium_since: Optional[datetime] = datetime.fromisoformat(data.get("premium_since"))
        else:
            self.premium_since = None

        self.joined_at = datetime.fromisoformat(data["joined_at"])

        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")
        self.pending: bool = data.get("pending")

        self.permissions: Optional[str] = data.get("permissions")


class PartialGuild:
    ...


class Guild:
    ...


class Integration:
    ...