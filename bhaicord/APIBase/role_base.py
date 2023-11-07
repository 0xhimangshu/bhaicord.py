import bhaicord

from typing import List

from bhaicord.models.role import Role


async def fetch_roles_from_guild_base(guild_id: int) -> List[Role]:
    client = bhaicord.CurrentClient.get_client()

    rs = await client.http.request(
        "GET",
        f"/guilds/{guild_id}/roles"
    )
    return list(map(
        Role, await rs.json()
    ))