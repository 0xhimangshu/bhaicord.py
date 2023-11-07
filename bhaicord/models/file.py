from typing import Union, Optional, Dict, Any, BinaryIO

import attr
import io


@attr.s
class File:
    """Represents a file object"""

    fp: Union[str, io.IOBase, io.TextIOBase] = attr.field(repr=False)
    """The content"""

    filename: str = attr.field(default="no_file_name.txt")
    """The filename"""

    description: Optional[str] = attr.field(
        default=None,
        repr=True,
        kw_only=True
    )
    """The description for the attachment"""

    content = attr.ib(init=False)

    @content.default
    def _set_file_content(self) -> Union[str, bytes]:

        if isinstance(self.fp, io.TextIOBase):
            return "".join(self.fp.readlines())

        if isinstance(self.fp, str):
            return self.fp

        if isinstance(self.fp, io.BufferedIOBase):
            return self.fp.read()

    def to_dict(self, index: int) -> Dict[str, Any]:
        return {
            "id": index,
            "filename": self.filename,
            "description": self.description
        }


class Attachment:

    def __init__(self, data: Dict[str, Any]):
        self.id: str = data["id"]
        self.filename: str = data["filename"]
        self.description: Optional[str] = data.get("description")
        self.content_type: Optional[str] = data.get("content_type")
        self.size: Optional[int] = data.get("size")
        self.url: Optional[str] = data.get("url")
        self.proxy_url: Optional[str] = data.get("proxy_url")
        self.height: Optional[int] = data.get("height")
        self.width: Optional[int] = data.get("width")
        # i don't know yet what ephemeral is

    # def to_dict(self) -> Dict[str, Any]:
    # """Attachment to dict"""
    # return from_obj_to_dict(self)
