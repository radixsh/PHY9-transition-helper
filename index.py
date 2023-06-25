import asyncio

import discord
from discord.ext import commands

from env import DEBUG_ID, PREFIX, TOKEN

DEBUG_SERVER = discord.Object(id=DEBUG_ID)

intents = discord.Intents.all()
intents.presences = intents.message_content = False
client = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX), intents=intents, help_command=None
)


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


@client.command(name="dev-sync", aliases=["dsync"], hidden=True)
@commands.is_owner()
async def dev_sync(ctx: commands.Context):
    """Sync current command tree to dev discord server"""
    client.tree.copy_global_to(guild=DEBUG_SERVER)
    await client.tree.sync(guild=DEBUG_SERVER)
    await ctx.send("Synced global command tree to development server")


@client.command(name="global-sync", hidden=True)
@commands.is_owner()
async def global_sync(ctx: commands.Context):
    """Sync current command tree to dev discord server"""
    await ctx.send("Initiating global sync...")
    await client.tree.sync()
    await ctx.reply(f"Synced global command tree to development server", mention_author=True)


@reload.error
@dev_sync.error
@global_sync.error
async def re_err(ctx: commands.Context, err):
    """Likely a permissions error. Should log this, once that's setup."""
    # FIXME: should probably log this
    return


@client.event
async def on_message(message: discord.Message):
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
