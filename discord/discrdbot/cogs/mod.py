from dis import disco
import discord
from discord.ext import commands
from datetime import timedelta
from discord import Colour, app_commands
from bot import MyBot

class Mod(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
    
    #clear command

    @app_commands.command(description="delete a speific ammount of messages from the channel")
    @app_commands.checks.has_role(1072854373115383828)
    async def clear(self, interaction:discord.Interaction, amount: int):
        await interaction.response.defer(thinking=True)
        clear_embed = discord.Embed(description = f"deleted {amount} messege(s)", colour=discord.Colour.red())
        await interaction.channel.purge(limit=amount+1)
        await interaction.channel.send(embed=clear_embed, delete_after=3)

    # @clear.error
    # async def on_error(self, interaction:discord.interactions, error:commands.CommandError):
    #     if isinstance(error, app_commands.MissingPermissions):
    #         await interaction.response.send_message(
    #             "You don't have permission to use this command.",
    #             ephemeral=True
    #             )

    #klick command

    @app_commands.command(description="kick a member from the server")
    @app_commands.checks.has_role(1072854373115383828)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        kick_embed = discord.Embed(description=f"{member} has been kicked for `{reason}`", colour=discord.Colour.red())
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=kick_embed, delete_after=10)
        kick_member = discord.Embed(description=f"You've been kicked out from Cloudy Skies for `{reason}`", colour=discord.Colour.red())
        await member.send(embed=kick_member)

    #ban command

    @app_commands.command(description="ban a member from the server")
    @app_commands.checks.has_role(1073060798043271228)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        ban_embed = discord.Embed(description=f"{member} has been banned for `{reason}`")
        await member.ban(reason=reason, delete_message_days=1)
        await interaction.response.send_message(embed=ban_embed, delete_after=10)
        ban_member = discord.Embed(description=f"You've been banned from Cloudy Skies for `{reason}`")
        await member.send(embed=ban_member)

    #warn command

    @app_commands.command(description="warn a member")
    @app_commands.checks.has_role(1072854373115383828)
    async def warn(self,
        interaction: discord.Interaction, member: discord.Member, *, reason: str):
        warn_embed = discord.Embed(description=f"{member} has been warned for `{reason}`", colour=discord.Colour.red())
        await interaction.response.send_message(embed=warn_embed ,delete_after=10)
        warn_member = discord.Embed(description=f"You have been warned for `{reason}`", colour=discord.Colour.red())
        await member.send(embed=warn_member)

    #dm command

    @app_commands.command(description= "Dm a member from the server")
    @app_commands.checks.has_role(1072854373115383828)
    async def dm(
        self, interaction: discord.Interaction, member: discord.Member, *, message: str
        ):
        await interaction.response.defer(thinking=True)
        dm_member = discord.Embed(description=message, colour=discord.Colour.yellow())
        await member.send(embed=dm_member)
        dm_embed = discord.Embed(
            description=f"Send `{message}` to {member}", color=discord.Color.yellow()
        )
        m = await interaction.followup.send(embed=dm_embed)
        await m.delete(delay=8)

    #timeout command

    @app_commands.command(description="timeout a member from the server")
    @app_commands.checks.has_role(1072854373115383828)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, *, reason: str):
        dm_embed = discord.Embed(description=f"{member} has been timed out for {reason}", colour=discord.Colour.orange())
        delta = timedelta(minutes=minutes)
        await member.timeout(delta, reason=reason)
        await interaction.response.send_message(embed=dm_embed, delete_after=10)

    #embed command

    @app_commands.command(name='embed',description='send an embed')
    @app_commands.checks.has_role(1072854373115383828)
    async def embed(self, interaction: discord.Interaction, title: str,
        messege: str, image_url: str, field_1: str,
        value_1: str, footer: str,
        ):
        member=interaction.user
        embed_message = discord.Embed(title=title, description=messege, colour=discord.Colour.orange())#or colour=0x00FFB3

        embed_message.set_author(name=f"Request by {member.display_name}", icon_url=member.avatar)
        embed_message.set_thumbnail(url=interaction.guild.icon.url)#or (url= the discord image url)
        embed_message.set_image(url=image_url)
        embed_message.add_field(name=field_1, value=value_1, inline=False)
        #embed_message.add_field(name="Field 2", value="value 2", inline=False)
        embed_message.set_footer(text=footer, icon_url=member.avatar)

        await interaction.response.send_message(embed = embed_message)

async def setup(bot: commands.bot):
    await bot.add_cog(Mod(bot))