import discord
import discord.ext.commands as commands


class TransitionCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["h"])
    async def help(self, ctx):
        # FIXME: this is a temporary hack because I don't want to spend a bunch of time fixing the
        # prefix in the help command immediately before removing the concept of prefixes altogether
        # Thus, it's just quickly hardcoded. Hoewver, once the migration to slash commands is done,
        # this entire help command system should probably be revisited.
        # We can also use newer UI features to make the help system potentially much nicer.
        PREFIX = ","
        embed = discord.Embed(
            title=f"Bot prefix: `{PREFIX}`",
            description=f"Role/channel/category duplicator bot. Note that command "
            "execution requires **Server Moderator** or **Server Moderator "
            "In-Training** role.",
            color=0xB2558D,
        )
        embed.add_field(
            name=f"`{PREFIX}erase some channel category`",
            value=f"_To be used quarterly._"
            "\nErases channel category. Deletes the role associated with the "
            "category."
            "\n_Note: the category must end with `[ARCHIVED]`._",
            inline=False,
        )
        embed.add_field(
            name=f"`{PREFIX}archive some channel category`",
            value=f"_To be used quarterly._"
            "\nMoves category to bottom of list and appends "
            "`[ARCHIVED]` to its name, enabling it to be deleted later. "
            "Deletes the role associated with the category. "
            "\n_Note: the category must start with `9` or `PHY`, and it "
            "must not contain the string `GLOBAL`._",
            inline=False,
        )
        embed.add_field(
            name=f"`{PREFIX}create some channel category`",
            value=f"_To be used quarterly._" "\nCreates a custom category and role.",
            inline=False,
        )
        embed.add_field(
            name=f"`{PREFIX}strip`",
            value=f"_To be used quarterly._"
            "\nStrips roles `9A`, `9B`, `9C`, `9D`, and `9H` from "
            "everyone.",
            inline=False,
        )
        embed.add_field(
            name=f"`{PREFIX}find some role`",
            value=f"Shows a list of people with the specified role.",
            inline=False,
        )
        embed.add_field(
            name=f"`{PREFIX}duplicate some channel category`",
            value=f"Duplicates channel category and its channels and "
            "roles/permissions. To be used only when a certain professor is "
            "teaching the same class this quarter as last quarter.",
            inline=False,
        )
        embed.set_footer(text="Contact radix.sh with issues.")
        return await ctx.send(embed=embed)

    @staticmethod
    def _find_match(needle, haystack):
        for category in haystack:
            if needle.lower() == category.name.lower():
                return category

    @staticmethod
    def _is_protected(category):
        return "global" in category.name.lower() or (
            not category.name.startswith("9") and not category.name.lower().startswith("phy")
        )

    @staticmethod
    async def _delete_role(role_name, ctx):
        # Just in case the user sent "9B Mitchell" like the category name
        role_name = role_name.replace(" ", "-")

        # _find_match() is not case-sensitive
        role = TransitionCommands._find_match(role_name, ctx.guild.roles)
        try:
            await role.delete()
            await ctx.send(f'Deleted role "{role_name}"')
        except:
            await ctx.send(f"Role not found :(")

    @commands.command(aliases=["remove", "delete", "purge", "nuke"])
    async def erase(self, ctx, *, arg):
        if not arg:
            return await ctx.send("Error: what category are you trying to erase?")

        if arg == "this":
            to_erase = ctx.channel.category
        else:
            to_erase = self._find_match(arg, ctx.guild.categories)
            if not to_erase:
                return await ctx.send(f"No such category found")

        if self._is_protected(to_erase) or "archive" not in to_erase.name.lower():
            return await ctx.send(f"Illegal!")

        for c in to_erase.channels:
            await c.delete()
        await to_erase.delete()

        # Quietly fail if the channel in which the command was sent has been deleted
        if arg != "this":
            await ctx.send(f"Successfully deleted category {to_erase.name}")

        # Attempt to delete the associated role, and quietly fail if impossible
        try:
            role_to_erase = to_erase.name.replace(" [ARCHIVED]", "").strip()
            await self._delete_role(role_to_erase, ctx)
        except:
            await ctx.send(
                f"Something went wrong trying to delete the role " "associated with this category"
            )

    @commands.command(aliases=["hide", "shelve"])
    async def archive(self, ctx, *, arg):
        if not arg:
            return await ctx.send("Error: what category are you trying to archive?")

        if arg == "this":
            # We choose the category that the command message was sent in
            to_archive = ctx.channel.category
        else:
            # We look for the matching category and choose any match
            to_archive = self._find_match(arg, ctx.guild.categories)
            if not to_archive:
                return await ctx.send(f"No such category found")

        # We are only allowed to delete categories whose names start with "9" (i.e.,
        # are in the format 9C Mitchell).
        if self._is_protected(to_archive):
            return await ctx.send(f"Illegal!")

        # Place the new category before the first category with [ARCHIVED] in its
        # name
        pos = len(ctx.guild.categories)
        name = to_archive.name
        for category in ctx.guild.categories:
            if "[archived]" in category.name.lower():
                pos = ctx.guild.categories.index(category) - 1
                break
        await to_archive.edit(name=f"{name} [ARCHIVED]", position=pos)

        # Attempt to delete the associated role, and quietly fail if impossible
        try:
            role_to_erase = to_archive.name.replace(" [ARCHIVED]", "").strip()
            await self._delete_role(role_to_erase, ctx)
        except Exception as e:
            await ctx.send(
                f"Something went wrong trying to delete the role "
                f"associated with this category: {e}"
            )

        return await ctx.send("Done :3")

    @commands.command(aliases=["add"])
    async def create(self, ctx, *, name=None):
        if not name:
            return await ctx.send("Error: what category are you trying to create?")

        # Transform "9c mitchell" to "9C Mitchell" for channel name
        name = [letter.capitalize() for letter in name.split(" ")]
        name[0] = name[0].upper()
        name = " ".join(name)

        # Create corresponding role
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

        # Place the new category before the first category that has [ARCHIVED] in
        # its name
        pos = len(ctx.guild.categories)
        for category in ctx.guild.categories:
            if "[archived]" in category.name.lower():
                pos = ctx.guild.categories.index(category) - 1
                break

        # Create the category
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

    @commands.command(aliases=[])
    async def strip(self, ctx):
        roles_to_strip = ["9A", "9B", "9C", "9D", "9H"]
        roles = []
        for role in roles_to_strip:
            roles.append(self._find_match(role, ctx.guild.roles))

        # Now the list is full of actual roles!
        count = 0

        # https://www.reddit.com/r/discordapp/comments/8yvq4g/get_all_users_with_a_role_using_discordpy/
        for member in ctx.guild.members:
            for role in member.roles:
                if role.name in roles:
                    await member.remove_roles(role)
                    count += 1
        # for role in roles:
        #     for member in role.members:
        #         await member.remove_roles(role)
        #         count += 1
        return await ctx.send(f"Removed roles {', '.join(roles_to_strip)} from {count} members :)")

    @commands.command(aliases=["list"])
    async def find(self, ctx, *, role_name):
        if not role_name:
            return await ctx.send(f"Error: what role are you trying to " "investigate?")

        role_name = role_name.lower()

        # role = None
        # for real_role in ctx.guild.roles:
        #     if real_role.name.lower() == role_name:
        #         role = real_role
        #         break
        role = self._find_match(role_name, ctx.guild.roles)
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

    @commands.command(aliases=["dup", "clone"])
    async def duplicate(self, ctx, *, arg):
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

        await old.edit(name=f"{old.name} [ARCHIVE]", position=1000)

        return await ctx.send("Done :3")


async def setup(bot: commands.Bot):
    await bot.add_cog(TransitionCommands(bot))
