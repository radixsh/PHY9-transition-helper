# Physics 9 transition helper 
This Discord bot was built for the UC Davis Physics 9 Discord server to automate
repetitive admin work done at the end of every quarter, such as archiving the
old channels that used to correspond with a particular professor's class.


## Functionalities
* `create some new channel category`: Creates a custom category and a matching
custom role, and limits the category to be visible only to that role. 
* `duplicate some existing channel category`: Duplicates a channel category (both its
channels and its permissions)
* `archive some existing channel category`: Moves category to bottom of server
and appends "[ARCHIVED]" to its name. This command is limited to categories
whose names are `9_ ______` and which do not contain the string `GLOBAL`.
* `erase some existing channel category`: Erases category and its channels. This
command is also limited to section-specific categories.
* `find some role`: Shows a list of people with the specified role.


## Technologies used
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [Discord API](https://discord.com/developers/docs/intro)
- [node.js](https://nodejs.org/en/)
- [nodemon](https://nodemon.io/)
    - [`nodemon --exec python3 hello.py`](https://stackoverflow.com/questions/65021005/how-to-run-python-3-with-nodemon)


## Usage
To get started, get a bot token and create an env.py:
```sh
TOKEN = 'your-discord-bot-token-here'
PREFIX = ','
```

Install discordpy if necessary (`python3 -m pip install discord`) before running
`python3 index.py`.

Note: Nothing, not even granting every single other permission, was enough for
the bot to function without admin permissions.

Add my instance 
[here](https://discord.com/api/oauth2/authorize?client_id=724415454604689421&permissions=8&scope=bot).


## License
Released under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). 
