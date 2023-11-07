from typing import TYPE_CHECKING, List, Optional, Iterable, Dict, Any, Union
import attr
import enum
import bhaicord

# UNIMPLEMENTED


class ActivityTypes(enum.Enum):
    game = 0
    streaming = 1
    listening = 2
    watching = 3
    custom = 4
    competing = 5


@attr.s
class Activity:
    """Discord Activity

    Arguments:
        name (str): The name
        type (typing.Union[int, discpy.models.presence.ActivityTypes]):
            The type of the activity
    """

    name: str
    type: Union[int, ActivityTypes] = attr.ib(default=ActivityTypes.listening.value)

    def to_dict(self) -> Dict[str, Any]:
        """Object to dictionary"""

        if isinstance(self.type, ActivityTypes):
            type_ = self.type.value
        else:
            type_ = self.type

        return {
            "name": self.name,
            "value": type_
        }


@attr.s
class Presence:
    """Discord presence"""
    activities: Optional[Iterable[Activity]] = attr.ib(default=None)

    status: str = attr.ib(default="online")

    def to_dict(self) -> List[Dict[str, Any]]:
        """Returns the dictionary of this object"""
        return {
            "status": self.status,
            "activities": [act.to_dict() for act in self.activities]
        }