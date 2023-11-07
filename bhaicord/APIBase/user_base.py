from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import bhaicord
    from bhaicord import User, CurrentClient

import bhaicord
from typing import Union


async def fetch_user_base(user_id: int) -> "User":
    """
    Gets a member object by id

    Args:
        user_id (int): user or member id

    it checks first if this user is already in cache
    if so, don't make a request but return the user
    If the user is not in cache add it
    but if cache size exceeded, just remove the first
    user from cache, and add the requested.
    """

    client = bhaicord.CurrentClient.get_client()

    user = client.user_cache.get(user_id)

    if user:
        return user

    if len(client.user_cache) >= client.cache_size:
        key = list(client.user_cache.keys())[0]

        del client.user_cache[key]

    rs = await client.http.request("GET", f"/users/{user_id}")
    user = bhaicord.User(await rs.json())

    client.user_cache[user.id] = user

    return user