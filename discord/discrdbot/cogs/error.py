import dis
from itertools import permutations
import discord
from discord.ext import commands
from bot import MyBot
from discord import Permissions, app_commands

class ErrorCog(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingRole):
            role = interaction.guild.get_role(error.missing_role)
            error_embed = discord.Embed(description=f"You  don't have permission to use these commands. {role.name} role needed", colour=discord.Colour.red())
            await interaction.response.send_message(embed=error_embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
        
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"Missing required agument - {error.param.name}.")

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send("Command not found.")

        elif isinstance(error, commands.MissingPermissions):
            perms = ""
            for p in error.missing_permissions:
                perms += f"{p},"

            return await ctx.send("You need {perms} to use this command.")

        else:
            raise error

async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorCog(bot))
