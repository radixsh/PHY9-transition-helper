# Duplicator bot
This Discord bot can duplicate a channel category's channels and roles/permissions.

To get started, get a bot token and create an env.py in this directory:
```sh
TOKEN = 'your-discord-bot-token-here'
PREFIX = ','
```

Install discordpy if necessary (`python3 -m pip install discord`) before running
`python3 index.py`.

Note: I tried granting the bot the `manage_channels` permission, but it still
complained about permissions errors when I tried to create channels, so I gave
up and gave my instance admin (the permissions integer was 8, making the link
look something like this:
https://discord.com/api/oauth2/authorize?client_id=724415454604689421&permissions=8&scope=bot.
If you figure out how to not require admin, please tell me the permissions
and/or permissions integer you chose so I can do it too. ^-^
