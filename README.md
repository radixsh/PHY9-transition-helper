# Physics 9 transition helper 
This Discord bot was built for the UC Davis Physics 9 Discord server to automate
repetitive admin work done at the end of every quarter, such as archiving the
old channels that used to correspond with a particular professor's class.


## Functionalities
### Commands for server transition between quarters
These commands should ideally be run in this order:
* `erase some existing channel category`: Erases channel category.
  Deletes the role associated with the category.
  * Note: the category must end with `[ARCHIVED]`.
* `archive some existing channel category`: Moves category to bottom of list and
  appends [ARCHIVED] to its name, enabling it to be deleted later.
  Deletes the role associated with the category.
  * Note: the category must start with `9` or `PHY`, and it must not
    contain the string `GLOBAL`.
* `create some new channel category`: Creates a custom category and a matching
  custom role, and limits the category to be visible only to that role.
* `strip`: Strips roles `9A`, `9B`, `9C`, `9D`, and `9H` from everyone.

### Other commands that may be useful
* `find some role`: Shows a list of people with the specified role.
* `duplicate some existing channel category`: Duplicates channel category
  and its channels and roles/permissions. To be used only when a certain
  professor is teaching the same class this quarter as last quarter.


## Technologies used
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [Discord API](https://discord.com/developers/docs/intro)
- [node.js](https://nodejs.org/en)
- [nodemon](https://nodemon.io)


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
