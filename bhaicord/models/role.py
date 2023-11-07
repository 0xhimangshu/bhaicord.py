from __future__ import annotations

from pydantic import BaseModel
from typing import (
    Optional,
    Union,
    Dict,
    Any,
    List
)
import bhaicord
from bhaicord.utils import simplify_attrs_from_dict, DataType, make_optional
from bhaicord.APIBase.image_base import make_role_icon


class RoleTags:

    def __init__(self, role_tags_data: DataType):

        self.bot_id: Optional[int] = make_optional(
            int,
            role_tags_data.get("id"))

        self.integration_id: Optional[int] = make_optional(
            int,
            role_tags_data.get("id"))

        self._premium_subscriber: Optional[int] = role_tags_data.get("premium_subscriber", 0)

    def is_premium_subscriber(self) -> bool:
        """Whether the role is premium subscriber"""
        return self._premium_subscriber is None

    def __repr__(self) -> str:
        return f"<RoleTags bot_id={self.bot_id}" \
               f" integration_id={self.integration_id}" \
               f" premium_subscriber={self._premium_subscriber}>"


class Role:

    def __init__(self, role_data: DataType):
        self.id: Optional[int] = role_data.get("id")
        self.name: Optional[str] = role_data.get("name")
        self.color: Optional[int] = role_data.get("color")
        self.colour = self.color
        self.hoist: Optional[bool] = role_data.get("hoist")
        self._icon: Optional[str] = role_data.get("icon")
        self.unicode_emoji: Optional[str] = role_data.get("unicode_emoji")
        self.position: int = role_data.get("position", 0)
        self._permissions: int = int(role_data.get("permissions", 0))
        self.managed: bool = role_data.get("managed", False)
        self.mentionable: bool = role_data.get("mentionable", False)
        self.tags: Optional[RoleTags] = make_optional(RoleTags, role_data.get("tags"))

    @property
    def permissions(self) -> int:
        # UNIMPLEMENTED
        return self._permissions

    @property
    def icon_url(self) -> Optional[str]:
        """The icon url"""
        return make_role_icon(self.id, self._icon)

    @staticmethod
    async def from_guild_id(id_: int) -> List[Role]:
        """Returns the role object by id"""

        return await bhaicord.fetch_roles_from_guild_base(id_)