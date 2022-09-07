import discord
from discord.ext import commands
from env import TOKEN, PREFIX

intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f'{PREFIX}help'))
    print("\nServers: ")
    for guild in client.guilds:
        print(f"- {guild.name} ({guild.member_count} members)")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

@client.command(aliases=['h'])
async def help(ctx):
    embed = discord.Embed(title=f"Bot prefix: `{PREFIX}`",
            description=f"Role/channel/category duplicator bot",
            color=0xb2558d)
    embed.add_field(name=f'`{PREFIX}duplicate some channel category here`',
            value=f'Duplicates channel category and its roles/permissions',
            inline=False)
    embed.set_footer(text="Contact radix#9084 with issues.")
    return await ctx.send(embed=embed)

@client.command(aliases=['up', 'u'])
async def uptime(ctx):
    current_time = datetime.now()
    delta = int((current_time - start_time).total_seconds())
    d, rem = divmod(delta, 24 * 60 * 60)
    h, rem = divmod(rem, 60 * 60)
    m, s = divmod(rem, 60)
    uptime = f"Uptime: `{d} day{'' if d == 1 else 's'}, "
    uptime += f"{h} hour{'' if h == 1 else 's'}, "
    uptime += f"{m} minute{'' if m == 1 else 's'}, "
    uptime += f"{s} second{'' if s == 1 else 's'}`"
    await ctx.send(uptime)

@client.command(aliases=['l'])
async def list(ctx, *args):
    ALL_ROLES = {}

    for m in ctx.guild.members:
        for role in m.roles:
            if role.name != "@everyone":
                if role.name in ALL_ROLES:
                    ALL_ROLES[role.name].append(f'`{m.name}#{m.discriminator}`')
                else:
                    ALL_ROLES[role.name] = [f'`{m.name}#{m.discriminator}`']

    for role in ALL_ROLES:
        long_list = f'**{role}**: {", ".join(ALL_ROLES[role])}\n'
        if len(long_list) < 2000:
            await ctx.send(long_list)
        else:
            parts = []
            for i in range(0, len(long_list), 1000):
                parts.append(long_list[i:i+1000])
            if len(parts) > 3:
                await ctx.send(f'(**{role}** has too many people in it to '
                        'list)')
            else:
                for part in parts:
                    await ctx.send(part)
    return

@client.command(aliases=['f'])
async def find(ctx, *, role):
    real_roles = []
    for real_role in ctx.guild.roles:
        real_roles.append(real_role.name)
    if role not in real_roles:
        return await ctx.send("That role does not exist!")

    people_in_role = []
    for m in ctx.guild.members:
        member_specific_roles = []
        for r in m.roles:
            member_specific_roles.append(r.name)
        if role in member_specific_roles:
            people_in_role.append(f'`{m.name}#{m.discriminator}`')

    if not people_in_role:
        return await ctx.send(f'No one with that role!')

    long_list = f'People with role `{role}`:\n'
    for person in people_in_role:
        long_list += f'{person}\n'
    parts = []
    for i in range(0, len(long_list)-1, 1900):
        temp = long_list[i:i+1900].rindex("\n")
        try:
            await ctx.send(long_list[i:temp])
        except:
            print(f'Failed to ctx.send: {long_list[i:temp]}')
    return

@client.command()
async def duplicate(ctx, *, arg):
    # TODO: Redo this all with querying by id instead of string name

    # Can't think of a more elegant way at this moment...
    old = ""
    stop = True
    for category in ctx.guild.categories:
        if arg == category.name:
            old = category 
            stop = False 
            break
    if stop:
        return await ctx.send(f"No such category found")

    # Copy the old category's roles/perms to the new category
    new = await ctx.guild.create_category(f"{old.name} duplicate",
            overwrites=old.overwrites)
    print(f"new ({type(new)}): {new}")

    for c in old.channels:
        if not c.permissions_synced:
            overwrites = c.overwrites
        else:
            overwrites = old.overwrites

        clone = await c.clone() 
        await clone.edit(category=new)
        print(clone)
        # await c.delete()

    # await old.delete()

    return await ctx.send("Done")

@client.command()
async def erase(ctx, *, arg):
    to_erase = ""
    stop = True
    for category in ctx.guild.categories:
        if arg == category.name:
            to_erase = category 
            stop = False 
            break
    if stop:
        return await ctx.send(f"No such category found")

    for c in to_erase.channels:
        await c.delete()
    await to_erase.delete()

client.run(TOKEN)
