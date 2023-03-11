import discord
from discord.ext import commands
from itsdangerous import json
from bot import MyBot
from discord import Guild, app_commands
import json

class Welcomer(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("discrdbot\data.json", "r") as f:
            records = json.load(f)

        try:
            channel_id = records[str(member.guild.id)]
        except KeyError:
            return

        channel = self.bot.get_channel(int(channel_id))
        if not channel:
            return
            
        welcomer_embed = discord.Embed(
            description=f"Welcome {member.mention}! You are {member.guild.member_count}th member of {member.guild.name}",
            colour=discord.Colour.blue()
        )
        await channel.send(embed=welcomer_embed)


    @app_commands.command(description="Select a welcome channel")
    @app_commands.checks.has_role(1073060798043271228)
    async def welcome(self, interation:discord.Interaction):
        with open("discrdbot\data.json", "r") as f:
            records = json.load(f)

        records[str(interation.guild_id)] = str(interation.channel_id)
        with open("discrdbot\data.json", "w") as f:
            json.dump(records, f)
        welcome_embed = discord.Embed(description=f"Success! {interation.channel.mention} is your welcome channel.", colour=discord.Colour.green())
        await interation.response.send_message(embed=welcome_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcomer(bot))