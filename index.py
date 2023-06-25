import asyncio

import discord
from discord.ext import commands
from env import TOKEN, PREFIX


intents = discord.Intents.all()
intents.presences = intents.members = False
client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


@client.check
async def require_admin(ctx: commands.Context):
    """Require all commands to be issued by a server administrator

    In the future, we might want to deal a little more granularly with permissions but
    for now, this seems fine to me. All relevant roles are administrator only, so it
    should be fine to use this for now.
    """
    return ctx.guild is not None and ctx.permissions.administrator


@client.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError):
    if isinstance(err, commands.CheckFailure):
        return await ctx.send("Invalid Permissions", ephemeral=True)
    await commands.Bot.on_command_error(client, ctx, err)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}help")
    )
    print("\nServers: ")
    for guild in client.guilds:
        print(f"- {guild.name} ({guild.member_count} members)")


@client.command()
@commands.is_owner()
async def reload(ctx: commands.Context):
    try:
        await client.reload_extension("transition_commands")
    except Exception as e:
        await ctx.send(f"Failed to load commands due to {e.__class__}: {e}")
        return
    await ctx.send("Complete")


@reload.error
async def re_err(ctx: commands.Context, err):
    """Likely a permissions error. Should log this, once that's setup."""
    # FIXME: should probably log this
    return


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


async def main():
    async with client:
        try:
            await client.load_extension("transition_commands")
        except Exception as e:
            print(f"Failed to load commands due to {e.__class__}: {e}")
        await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
