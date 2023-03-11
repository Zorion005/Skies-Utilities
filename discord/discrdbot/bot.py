from email import utils
import random
from webbrowser import get
from async_timeout import timeout
import discord
from discord.ext import commands, tasks
from itertools import cycle
import config
import asyncio

exts = [
    "cogs.mod",
    "cogs.welcomer",
    "cogs.error"
]

bot_status = cycle([
    "Watchig everyone",
    "Clash of Clans"
    ])
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Red", description="Red is a colour", emoji="<:clashgoblin35:1082591560996233247>", value="red"),
            discord.SelectOption(label="Blue", description="Blue is a colour", emoji="<:clashduh:1082591555002576987>", value="blue"),
            discord.SelectOption(label="Green", description="Green is a colour", emoji="<:clashhuh5:1082591593145581639>", value="green"),
            discord.SelectOption(label="Yellow", description="Yellow is a colour", emoji="<:clashkiss45:1082591598170361896>", value="yellow"),
            discord.SelectOption(label="Purple", description="Purple is a colour", emoji="<:clashhappy:1082591567132499968>", value="purple"),
        ]

        super().__init__(placeholder="Select an option", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected {self.values[0]}")

class close(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, row=1)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("closed the dropdown", ephemeral=True)
        await self.message.delete()
        self.stop()
        

class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, intents:discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        for ext in exts:
            await self.load_extension(ext)
            print("Success: Cog file loaded")

    async def on_ready(self):
        print(f'Success: Logged in as {bot.user} (ID: {bot.user.id})')

        change_status.start()
        print("Success: Status changing")

class Prompt(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60.0)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Yes", emoji="<:CHECK_CHECK_1:1076751205667196929>")
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        yes_embed = discord.Embed(description="You said yes!", color=discord.Color.green())
        await interaction.response.send_message(embed=yes_embed)
        await self.message.delete()
        self.stop()

    @discord.ui.button(style=discord.ButtonStyle.red,label="No", emoji="<:CHECK_CROSS_1:1076751294628376626>")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        no_embed = discord.Embed(description="You said no!", color=discord.Color.red())
        await interaction.response.send_message(embed=no_embed)
        await self.message.delete()
        self.stop()

class SelfRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Red")
    async def red_color(self, interaction: discord.Interaction, button:discord.ui.Button):
        red_role = discord.utils.get(interaction.guild.roles, name="Red")

        await interaction.user.add_roles(red_role)

if __name__=="__main__":
    bot = MyBot(command_prefix="-", intents=discord.Intents.all())
    
    
    #  MESSAGE COMMANDS

    @bot.command(name="selfroles")
    async def self_role(ctx):
        await ctx.send("Give your self a role",view = SelfRoles())

    @bot.command()
    async def dropdown(ctx):
        view = discord.ui.View(timeout=60)
        view = close()
        view.add_item(Dropdown())

        view.message=await ctx.send("Select a colour", view=view)

    @bot.command()
    async def button(ctx):
        view = Prompt()
        view.add_item(discord.ui.Button(label="Invite", url="https://discord.gg/pypUFSqWHB"))
        prompt_embed = discord.Embed(description="Do you want to continue?", color=discord.Color.yellow())
        view.message=await ctx.send(embed=prompt_embed, view=view)

    @bot.command()
    async def ping(ctx):
        await ctx.send("Pong")

    @bot.command()
    async def hi(ctx):
        with open("discrdbot\hi.txt", "r") as f:
            random_hi = f.readlines()
            response_hi = random.choice(random_hi)
        
        await ctx.send(response_hi)
        
    @bot.command()
    async def jokes(ctx):
        with open("discrdbot\jokes.txt", "r", encoding="utf-8") as j:
            random_joke = j.readlines()
            response_joke = random.choice(random_joke)
        
        await ctx.send(response_joke)

    @bot.command()
    async def userinfo(ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        info_embed = discord.Embed(title=f"{member.name}'s User Information", description="All information about this user.", color=member.color)
        info_embed.set_thumbnail(url=member.avatar)
        info_embed.add_field(name="**Name**", value=member.name, inline=False)
        info_embed.add_field(name="**Nick Name**", value=member.display_name, inline=False)
        info_embed.add_field(name="**Discriminator**", value=member.discriminator, inline=False)
        info_embed.add_field(name="**ID**", value=member.id, inline=False)
        info_embed.add_field(name="**Top Role**", value=member.top_role, inline=False)
        info_embed.add_field(name="**Status**", value=member.status, inline=False)
        info_embed.add_field(name="**Bot User**", value=member.bot, inline=False)
        info_embed.add_field(name="**Creation Date**", value=member.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"), inline=False)

        await ctx.send(embed=info_embed)




    @bot.command()
    @commands.is_owner()
    async def sync(ctx):
        await bot.tree.sync()
        await ctx.reply("Synced!")

    bot.run(config.DISCORD_TOKEN)