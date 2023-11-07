from .client import Client
from .intents import Intents
from .utils import *

from bhaicord.http import HTTPClient
from . import errors, models, websocket, APIBase, events

from .models.file import *
from .models.guild import *
from .models.message import *
from .models.user import *
from .models.presence import *
from .models.embed import *
from .models.color import *
from .models.channel import *
from .models.emoji import *
from .models.role import *
from .models.webhook import *

from .events.channel_events import *
from .events.message_events import *
from .events.ready_event import *
from .events.typing_start import *

from .errors.general import *
from .errors.http import *

from .APIBase.channel_base import *
from .APIBase.image_base import *
from .APIBase.message_base import *
from .APIBase.user_base import *
from .APIBase.role_base import *

__version__ = "0.0.1"
__author__ = "himangshu147-git"
__github__ = f"https://github.com/{__author__}/bhaicord.py"

gateaway_url = "wss://gateway.discord.gg"
api_url = "https://discord.com/api/v9"
cdn_url = "https://cdn.discordapp.com"

class CurrentClient:

    client: 'Client' = None

    @classmethod
    def get_client(cls) -> Optional['Client']:
        """Fetches the current client

        Raises:
            ClientNotFound: if the client wasn't found
        """
        if not cls.client:
            raise ClientNotFound

        return cls.client