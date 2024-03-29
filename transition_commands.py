import difflib
import logging
import re
from typing import Optional

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands
from discord import Interaction
from discord.app_commands import Choice

MATCH_HEURISTIC = 1.0


class TransitionCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger("discord.bot.transition")
        self._unarchived_pattern = re.compile(r"9[A-D]H?\s+[-\w]+", re.IGNORECASE)
        self._archived_pattern = re.compile(r"9[A-D]H?\s+\w+\s+\[ARCHIVED?\]", re.IGNORECASE)

    def cog_check(self, ctx: commands.Context):
        """Require all transition commands to be issued by an admin

        In the future, we might want to deal a little more granularly with permissions but
        for now, this seems fine to me. All relevant roles are administrator only, so it
        should be fine to use this for now.
        """
        self.logger.debug("Command cog-wide check")
        return ctx.guild is not None and ctx.permissions.administrator

    def interaction_check(self, interaction: Interaction) -> bool:
        """See cog_check method"""
        self.logger.debug(
            "Interaction cog-wide check: Guild: %s, perms: %x",
            interaction.guild_id,
            interaction.permissions.value,
        )
        return interaction.guild is not None and interaction.permissions.administrator

    @staticmethod
    async def base_autocomplete(
        interaction: Interaction, curr: str, pattern: re.Pattern
    ) -> list[Choice[str]]:
        if interaction.guild is None:
            return []
        # Select valid categories based on given pattern
        categories = [
            cat
            for cat in interaction.guild.categories
            if pattern.fullmatch(cat.name) and "global" not in cat.name.lower()
        ]
        if len(curr) == 0:
            return [app_commands.Choice(name=cat.name, value=cat.name) for cat in categories]
        # Find similarity of each category name
        similarities: dict[app_commands.Choice, float] = {}
        curr = curr.lower()
        for cat in categories:
            sim = difflib.SequenceMatcher(lambda x: x.isspace(), curr, cat.name.lower()).ratio()
            # TODO: debug log this
            # print(f"{curr} match {cat.name}: {sim}\n {sim * ((len(cat.name) + 1) / len(curr))**2}\n")
            if sim * ((len(cat.name) + 1) / len(curr)) ** 2 >= MATCH_HEURISTIC:
                similarities[app_commands.Choice(name=cat.name, value=cat.name)] = sim
        return sorted(similarities.keys(), key=lambda x: similarities[x], reverse=True)

    @app_commands.command(description="Get help for commands")
    async def help(
        self,
        interaction: Interaction,
    ):
        PREFIX = "/"
        embed = discord.Embed(
            title=f"PHY9 Transition Helper",
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
        embed.set_footer(text="Contact radix.sh with issues.")
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @staticmethod
    def match_case_insensitive_name(needle: str, haystack):
        for category in haystack:
            if needle.lower() == category.name.lower():
                return category

    @staticmethod
    def _is_protected(category):
        return "global" in category.name.lower() or (
            not category.name.startswith("9") and not category.name.lower().startswith("phy")
        )

    async def delete_role(self, role_name: str, interaction: Interaction):
        # Just in case the user sent "9B Mitchell" like the category name
        role_name = role_name.replace(" ", "-")

        # We require that all commands in this cog are guild only, so guild.roles cannot be None
        role = TransitionCommands.match_case_insensitive_name(role_name, interaction.guild.roles)  # type: ignore
        await role.delete()  # type: ignore  --- if None, will error, caller handles this
        self.logger.info("Deleted role %s", role_name)

    async def get_valid_category(
        self, interaction: Interaction, arg: Optional[str]
    ) -> Optional[discord.CategoryChannel]:
        if not arg:
            await interaction.response.send_message("Error: what category are you trying to erase?")
            return
        category: Optional[discord.CategoryChannel] = None
        if arg == "this":
            if hasattr(interaction.channel, "category"):
                category = interaction.channel.category  # type: ignore
        else:
            # Again, cog-wide check guarantees we are in a guild.
            category = self.match_case_insensitive_name(arg, interaction.guild.categories)  # type: ignore
        if not category:
            await interaction.response.send_message("No such category found")
            return
        if self._is_protected(category):
            self.logger.info(
                "%s requested mutation of invalid category %s", interaction.user.name, category.name
            )
            await interaction.response.send_message(
                f"Permission denied: cannot mutate non-section category {category}"
            )
            return
        return category

    @app_commands.command(description="Erase specified category")
    @app_commands.describe(category="Category to erase")
    async def erase(self, interaction: Interaction, category: Optional[str]):
        to_erase = await self.get_valid_category(interaction, category)
        if not to_erase:
            return
        self.logger.info("%s requested deletion of %s", interaction.user.name, to_erase.name)
        if "archive" not in to_erase.name.lower():
            self.logger.info(
                "%s requested deletion of invalid category %s", interaction.user.name, to_erase.name
            )
            return await interaction.response.send_message(
                f"Permission denied: cannot erase non-archived category {to_erase}"
            )
        await interaction.response.defer()
        for c in to_erase.channels:
            await c.delete()
        name = to_erase.name
        await to_erase.delete()
        # Don't send feedback if context channel was just deleted
        if category != "this":
            await interaction.followup.edit_message(
                (await interaction.original_response()).id, content=f"Erased category {name}"
            )
        # Attempt to delete the associated role, and quietly fail if impossible
        # TODO: do we need to keep this? role should be deleted in the archive process already.
        role_to_erase = to_erase.name.replace(" [ARCHIVED]", "").strip()
        try:
            await self.delete_role(role_to_erase, interaction)
        except:
            self.logger.info("Role deletion of %s failed", role_to_erase)

    @erase.autocomplete("category")
    async def erase_ac(self, interaction: Interaction, curr: str) -> list[Choice[str]]:
        return await self.base_autocomplete(interaction, curr, self._archived_pattern)

    @app_commands.command(description="Archive specified category")
    @app_commands.describe(category="Category to archive")
    async def archive(self, interaction: Interaction, category: Optional[str]):
        if interaction.guild is None:
            self.logger.error("Archive guild None")
            return await interaction.response.send_message("Internal Error :(")
        to_archive = await self.get_valid_category(interaction, category)
        # The second check isn't strictly necessary but it makes type checkers happy.
        if to_archive is None:
            return
        self.logger.info("%s requested archive of %s", interaction.user.name, to_archive.name)
        await interaction.response.defer()
        # Place the new category before the first category with [ARCHIVED] in its name
        pos = len(interaction.guild.categories)
        name = to_archive.name
        for cat in interaction.guild.categories:
            if "[archived]" in cat.name.lower():
                pos = interaction.guild.categories.index(cat) - 1
                break
        self.logger.debug("Move %s to position %d", to_archive.name, pos)
        await to_archive.edit(name=f"{name} [ARCHIVED]", position=pos)
        # Attempt to delete the associated role, and quietly fail if impossible
        role_to_erase = name.replace(" [ARCHIVED]", "").strip()
        try:
            await self.delete_role(role_to_erase, interaction)
        except Exception as e:
            self.logger.error("Error deleting role %s: %s", role_to_erase, e)
            await interaction.followup.edit_message(
                (await interaction.original_response()).id,
                content=f"Archived category {name}\n"
                f"Something went wrong deleting the role associated with this category.",
            )
            return
        await interaction.followup.edit_message(
            (await interaction.original_response()).id, content=f"Archived category {name}"
        )

    @archive.autocomplete("category")
    async def archive_ac(self, interaction: Interaction, curr: str) -> list[Choice[str]]:
        return await self.base_autocomplete(interaction, curr, self._unarchived_pattern)

    @app_commands.command(description="Create specified category")
    @app_commands.describe(name="Name of category")
    async def create(self, interaction: Interaction, name: Optional[str]):
        if not name:
            return await interaction.response.send_message(
                "Error: what category are you trying to create?"
            )
        # Again, not strictly necessary, but we aren't trying to maximize performance here and
        # this hints to the type checker that this can't be none, which is already checked in
        # a more user friendly way in the cog_check.
        if interaction.guild is None:
            self.logger.error("Create guild None")
            return await interaction.response.send_message("Internal Error :(")

        self.logger.info("%s requested creation of %s", interaction.user.name, name)
        await interaction.response.defer()
        # Transform "9c mitchell" to "9C Mitchell" for channel name
        name_split = [word.capitalize() for word in name.split(" ")]
        name_split[0] = name_split[0].upper()
        name = " ".join(name_split)
        # Create corresponding role
        hyphenated_name = name.replace(" ", "-")
        new_role = await interaction.guild.create_role(name=hyphenated_name)

        # https://stackoverflow.com/questions/64528917/adding-channel-overwrites-for-user-in-discord-py
        # https://stackoverflow.com/questions/63975108/creating-a-category-in-discordpy-with-permissions-that-only-a-specific-role-can
        # Hide this category from view by default
        base_perms = discord.PermissionOverwrite()
        base_perms.read_messages = False
        base_perms.send_messages = False
        # But allow those with the new role to see it
        course_role_perms = discord.PermissionOverwrite()
        course_role_perms.read_messages = True
        course_role_perms.send_messages = True
        overwrites = {interaction.guild.default_role: base_perms, new_role: course_role_perms}

        # Place the new category before the first category that has [ARCHIVED] in
        # its name
        pos = len(interaction.guild.categories)
        for category in interaction.guild.categories:
            if "[archived]" in category.name.lower():
                pos = interaction.guild.categories.index(category) - 1
                break

        # Create the category
        new_category = await interaction.guild.create_category(
            name=name, overwrites=overwrites, position=pos  # type: ignore
        )

        # Populate the new category with channels
        await new_category.create_text_channel("announcements")
        await new_category.create_text_channel("general")
        await new_category.create_text_channel("homework")
        await new_category.create_text_channel("discussion")
        await new_category.create_voice_channel(name)
        self.logger.info("Created new category %s", name)
        await interaction.followup.edit_message(
            (await interaction.original_response()).id, content=f"Created new category {name}."
        )

    @app_commands.command(description="Remove 9A, 9B, etc. roles from users.")
    async def strip(self, interaction: Interaction):
        # Again, this is for the benefit of type checkers
        if interaction.guild is None:
            self.logger.error("Strip guild None")
            return await interaction.response.send_message("Internal Error :(")
        await interaction.response.defer()
        roles_to_strip = ["9A", "9B", "9C", "9D", "9H"]
        roles: list[discord.Role] = []
        for role in roles_to_strip:
            r = self.match_case_insensitive_name(role, interaction.guild.roles)
            if r is not None:
                roles.append(r)
        # Now the list is full of actual roles!
        count = 0
        for role in roles:
            for member in role.members:
                await member.remove_roles(role)
                count += 1
        response_str = f"Removed roles {', '.join(roles_to_strip)} from {count} members."
        self.logger.info(response_str)
        await interaction.followup.edit_message(
            (await interaction.original_response()).id,
            content=response_str,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(TransitionCommands(bot))
