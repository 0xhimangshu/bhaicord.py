# bhaicord.py

### A simple discord api wrapper made in python

## Installation

```bash
pip install bhaicord.py
# or
pip install git+https://github.com/himangshu147-git/bhaicord.py.git
```

## Usage

```python
import bhaicord
from bhaicord import Client, Intents

client = Client(intents=Intents.all())


@client.event
async def on_ready(event):
    print("Bot is ready")


@client.event
async def message_create(msg: bhaicord.Message):
    if msg.content.startswith("test"):
        await msg.send("it works fine")

client.run("TOKEN")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
