import discord
from discord.ext import commands
from env import TOKEN, PREFIX

intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name=f"{PREFIX}help"
        )
    )
    print("\nServers: ")
    for guild in client.guilds:
        print(f"- {guild.name} ({guild.member_count} members)")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(
        title=f"Bot prefix: `{PREFIX}`",
        description=f"Role/channel/category duplicator bot",
        color=0xB2558D,
    )
    embed.add_field(
        name=f"`{PREFIX}create some channel category`",
        value=f"Creates a custom category accessible only to the "
        "corresponding role of the same name.",
        inline=False,
    )
    embed.add_field(
        name=f"`{PREFIX}duplicate some channel category`",
        value=f"Duplicates channel category and its channels and roles/permissions",
        inline=False,
    )
    embed.add_field(
        name=f"`{PREFIX}archive some channel category here`",
        value=f"Moves category to bottom of server and appends "
        '"[ARCHIVED]" to its name. Note: the '
        "category must be `9_ _____` AND not contain the string "
        "`GLOBAL`.",
        inline=False,
    )
    embed.add_field(
        name=f"`{PREFIX}erase some channel category`",
        value=f"Erases channel category and its channels. Note: the "
        "category must be `9_ _____` AND not contain the string "
        "`GLOBAL`.",
        inline=False,
    )
    embed.add_field(
        name=f"`{PREFIX}find some role`",
        value=f"Shows a list of people with the specified role",
        inline=False,
    )
    embed.set_footer(text="Contact radix#9084 with issues.")
    return await ctx.send(embed=embed)


@client.command(aliases=["list"])
async def find(ctx, *, role_name):
    role_name = role_name.lower()
    role = None
    for real_role in ctx.guild.roles:
        if real_role.name.lower() == role_name:
            role = real_role
            break
    if role is None:
        return await ctx.send("That role does not exist!")

    if not role.members:
        return await ctx.send(f"No one with that role!")

    long_list = [f"People with role `{role_name}`:"]
    for person in role.members:
        long_list.append(str(person))
    paginator = commands.Paginator()
    for line in long_list:
        if len(line) + len(paginator) > 2000:
            paginator.close_page()
        paginator.add_line(line)
    for page in paginator.pages:
        await ctx.send(page)


@client.command(aliases=["dup", "clone"])
@commands.has_any_role("Server Moderator", "Server Moderator In-Training")
async def duplicate(ctx, *, arg):
    old = ""
    stop = True
    for category in ctx.guild.categories:
        if arg.lower() == category.name.lower():
            old = category
            stop = False
            break
    if stop:
        return await ctx.send(f"No such category found")

    # Copy the old category's roles/perms to the new category
    new = await ctx.guild.create_category(
        f"{old.name}", overwrites=old.overwrites, position=old.position
    )

    for c in old.channels:
        if not c.permissions_synced:
            overwrites = c.overwrites
        else:
            overwrites = old.overwrites

        clone = await c.clone()
        await clone.edit(category=new)

    await old.edit(name=f"{old.name} [Archived by Duplicator]", position=1000)

    return await ctx.send("Done :3")


@client.command(aliases=["add"])
@commands.has_any_role("Server Moderator", "Server Moderator In-Training")
async def create(ctx, *, name):
    name = [p.capitalize() for p in name.split(" ")]
    name[0] = name[0].upper()
    name = " ".join(name)
    hyphenated_name = name.replace(" ", "-")
    new_role = await ctx.guild.create_role(name=hyphenated_name)

    # https://stackoverflow.com/questions/64528917/adding-channel-overwrites-for-user-in-discord-py
    # https://stackoverflow.com/questions/63975108/creating-a-category-in-discordpy-with-permissions-that-only-a-specific-role-can
    # Hide this category from view by default
    pleb_overwrite = discord.PermissionOverwrite()
    pleb_overwrite.read_messages = False
    pleb_overwrite.send_messages = False
    # But allow those with the new role to see it
    patrician_overwrite = discord.PermissionOverwrite()
    patrician_overwrite.read_messages = True
    patrician_overwrite.send_messages = True
    overwrites = {ctx.guild.default_role: pleb_overwrite, new_role: patrician_overwrite}

    # Place the new category before the first category with [ARCHIVED] in its
    # name
    pos = len(ctx.guild.categories)
    for category in ctx.guild.categories:
        if "[archived]" in category.name.lower():
            pos = ctx.guild.categories.index(category) - 1
            break

    await ctx.send(f"Creating new category {name}")
    new_category = await ctx.guild.create_category(
        name=name, overwrites=overwrites, position=pos
    )

    # Populate the new category with channels
    await new_category.create_text_channel("announcements")
    await new_category.create_text_channel("general")
    await new_category.create_text_channel("homework")
    await new_category.create_text_channel("discussion")
    await new_category.create_voice_channel(name)

    return await ctx.send("Done :3")


def find_match(needle, haystack):
    for category in haystack:
        if needle.lower() == category.name.lower():
            return category


def is_protected(category):
    return "global" in category.name.lower() and (
        not category.name.startswith("9") or not category.name.lower().startswith("phy")
    )


@client.command(aliases=["hide", "shelve"])
@commands.has_any_role("Server Moderator", "Server Moderator In-Training")
async def archive(ctx, *, arg):
    if arg == "this":
        # We choose the category that the command message was sent in
        to_archive = ctx.channel.category
    else:
        # We look for the matching category and choose any match
        to_archive = find_match(arg, ctx.guild.categories)
        if not to_archive:
            return await ctx.send(f"No such category found")

    # We are only allowed to delete categories whose names start with "9" (i.e.,
    # are in the format 9C Mitchell).
    if is_protected(to_archive):
        return await ctx.send(f"Illegal!")

    # Place the new category before the first category with [ARCHIVED] in its
    # name
    pos = len(ctx.guild.categories)
    for category in ctx.guild.categories:
        if "[archived]" in category.name.lower():
            pos = ctx.guild.categories.index(category) - 1
            break
    await to_archive.edit(name=f"{str(to_archive)} [ARCHIVED]", position=pos)

    return await ctx.send("Done :3")


@client.command(aliases=["remove", "delete", "purge", "nuke"])
@commands.has_any_role("Server Moderator", "Server Moderator In-Training")
async def erase(ctx, *, arg):
    if arg == "this":
        to_erase = ctx.channel.category
    else:
        to_erase = find_match(arg, ctx.guild.categories)
        if not to_erase:
            return await ctx.send(f"No such category found")

    if is_protected(to_erase):
        return await ctx.send(f"Illegal!")

    for c in to_erase.channels:
        await c.delete()
    await to_erase.delete()

    try:
        await ctx.send(f"Successfully deleted category {to_erase.name}")
    except:
        pass


@client.command(aliases=[])
@commands.has_any_role("Server Moderator", "Server Moderator In-Training")
async def strip(ctx):
    roles_to_strip = ["9A", "9B", "9C", "9D", "9H"]
    roles = []
    for role in roles_to_strip:
        roles.append(find_match(role, ctx.guild.roles))

    # Now the list is full of actual roles!
    count = 0
    for role in roles:
        for member in role.members:
            await member.remove_roles(role)
            count += 1
    return await ctx.send(f"Removed roles {', '.join(roles_to_strip)} from {count} members :)")


client.run(TOKEN)
