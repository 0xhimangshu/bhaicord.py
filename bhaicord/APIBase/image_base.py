from typing import Optional, Union
import bhaicord


def make_image_url(
        user_id: Union[str, int],
        hash_: Optional[str],
        size: int, *,
        avatar: bool = True,
        tag: Optional[int] = None) -> Optional[str]:

    """Builds the user or member avatar
    through the avatar hash.

    If the avatar hash is None, returns None

    Args:
        user_id (typing.Union[int, str]): The user id
        hash_ (str): the member's avatar hash or banner's hash
        size (int): The size, max is 4096, min is 16
        avatar (bool): If avatar is False, it will take banner's url
        tag (typing.Optional[int]): The user tag in case avatar hash is None

    Raises:
        cordic.errors.SizeOutOfBounds: when size out of bounds

    Return:
        typing.Optional[str]: URL or None
    """
    if size > 4096 or size < 16:
        raise bhaicord.SizeOutOfBounds

    if hash_ is None:
        if tag is None:
            return

        return bhaicord.APIBase.default_av_url.format(
            bhaicord.cdn_url,
            tag % 5
        )

    if hash_.startswith("a_"):
        # it's animated
        hash_ += ".gif"
    else:
        hash_ += ".png"

    url = bhaicord.APIBase.avatar_base_url if avatar else bhaicord.APIBase.banner_base_url

    return url.format(
        bhaicord.cdn_url,
        user_id,
        hash_,
        size
    )


def make_application_image(id_: int, hash_: str) -> Optional[str]:
    """Make application image, icon or cover

    Args:
        id_ (int): Id of the application
        hash_ (str): Either cover or icon hash
    """
    if hash_ is not None:
        return bhaicord.cdn_url + f"/app-icons/{id_}/{hash_}.png"


def make_role_icon(id_: int, icon: str) -> Optional[str]:
    """Make the role icon url"""

    if icon is not None:
        return bhaicord.cdn_url + f"/role-icons/{id_}/{icon}.png"