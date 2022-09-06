# Bitz? Quartz?
Qubitz is an uwubot and a music bot that can upload custom emojis and help you
find people by their roles.

I began developing an uwubot named Bitz for Discord in June 2020, in discord.js
because the first guides I found were in JavaScript. This turned out to be very
misguided, because (as I realized when our AP Computer Science Principles
teacher taught us Python and the basics of discord.py later that year)
discord.py is far superior. Over the summer of 2020, I developed and hosted both
bots on my Chromebook. Sometime or other I also spun up another discord.py bot,
Amicitia, to help students in a university Discord server find people with the
same major (majors being defined in roles).

I've wanted to translate Bitz's uwubot functionalities to Python for a while,
and I finally did, almost two years later. Bitz, the original uwubot I created,
has been translated to Python and conflated with Quartz's capabilities to form
Qubitz.

## Functionalities
Qubitz's functionalities include:
- `ping`: Pokes Qubitz to see if they're awake.
- `uptime`: Displays how long Qubitz has been awake.
- `create_emoji [name]`: Sets attached image as a custom server emoji with the
  given name.
- `info`: Gets guild and user information.
- `uwuify [any message here]`: Uwuifies your message, deleting the comand
  message.
- `echo [any message here]`: Echoes back your message, deleting the command
  message.
- `cat`: Shows a cat from [The Cat API](https://api.thecatapi.com/v1/images/search).
- `list`: Lists each role and everyone in them.
- `find [any role here]`: Prints a list of everyone with the given role.
- `play [any YouTube search term here]`: Searches YouTube and streams the audio
  of the first result in vc.
- `now_playing`: Displays the currently playing song.
- `queue`: Displays the song queue.
- `remove`: Removes a song from the queue.
- `skip`: Skips the currently playing song.
- `stop`: Disconnects Qubitz from vc and clears the song queue.

## Technologies
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [Discord API](https://discord.com/developers/docs/intro)
- [node.js](https://nodejs.org/en/)
- [nodemon](https://nodemon.io/)
- [The Cat API](https://thecatapi.com/)

## Usage
To set Qubitz up locally, you'll need `python3` and the packages for `discord`,
`requests`, and `aiohttp`.

You'll also need an API token, which you get by creating an application in your
Discord [developer portal](https://discord.com/developers/applications). Click
the subheading "bot" in the menubar on the left and add a bot, and a secret
token will have been generated under the bot's username.

Create a file called `env.py` with this as its contents:
```sh
TOKEN = "your-token-here-between-quotes"
```

In the developer portal again, under Bot, enable the server members and message
content intents. Under OAuth2 > URL Generator, generate an
[invite link](https://discord.com/api/oauth2/authorize?client_id=812437788535423008&permissions=3468352&scope=bot)
by selecting the "bot" scope and adding the following permissions:
- Read Messages / View Channels
- Send Mesages
- Manage Messages
- Embed Links
- Attach Files
- Use External Emojis
- Add Reactions

Then you can run Qubitz with `python3 index.py` (or `nodemon --exec python3
index.py`).

## Acknowledgements
- [aiohttp documentation](https://docs.aiohttp.org/en/stable/client.html),
  especially [this comparison](https://docs.aiohttp.org/en/stable/http_request_lifecycle.html#aiohttp-request-lifecycle) between aiohttp and requests
- [discord.js guide](https://discordjs.guide/)
    - [Getting user input](https://discordjs.guide/creating-your-bot/commands-with-user-input.html#basic-arguments)
    - [Adding more commands](https://discordjs.guide/creating-your-bot/adding-more-commands.html)
    - [Creating embeds](https://discordjs.guide/popular-topics/embeds.html#embed-preview)
    - [Some basic es6 syntax examples](https://discordjs.guide/additional-info/es6-syntax.html#template-literals)
    - [Dynamically executing commands](https://discordjs.guide/command-handling/dynamic-commands.html#dynamically-executing-commands)
    - [Miscellaneous examples](https://discordjs.guide/popular-topics/miscellaneous-examples.html#play-music-from-youtube),
    including playing music from YouTube and retrieving emoji characters from
    another file created in the same directory as index.js
- [How to create a music bot](https://www.freecodecamp.org/news/how-to-create-a-music-bot-using-discord-js-4436f5f3f0f8/) (Free Code Camp)
- [Adding a config file](https://anidiots.guide/first-bot/adding-a-config-file)
    (An Idiot's Guide) – This was helpful for conceptualizing the flow of order
    when the bot is running under `nodemon`. Using a config file taught me how
    the config file responds to calls from the index file.
    - [Understanding roles and permissions](https://anidiots.guide/understanding/roles)
- And, of course, places where people before me have asked questions:
    - [Get a picture from a message](https://stackoverflow.com/questions/55206958/get-a-picture-from-the-message) (Stack Overflow)
    - [Take file as argument](https://stackoverflow.com/questions/59181208/discord-py-bot-take-file-as-argument-to-command) (Stack Overflow)
    - [Discord bot send attachments](https://www.reddit.com/r/learnpython/comments/9ishxs/discord_bot_send_attachments/e6m0trf/) (Reddit): pointed me to aiohttp
    - [Using nodemon with python3](https://stackoverflow.com/questions/65021005/how-to-run-python-3-with-nodemon) (Stack Overflow)
- [Eric Yeung's Discord music bot](https://github.com/eric-yeung/Discord-Bot/blob/master/main.py)
  (GitHub)
- discord.py documentation, particularly:
    - [Cog documentation](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#cog)
        - [Coggification example](https://stackoverflow.com/questions/53528168/how-do-i-use-cogs-with-discord-py)
          (Stack Overflow)
    - [Voice client documentation](https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.voice_clients)

Bitz was named by my close friend Tumega500#1234.

## License
Released under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
