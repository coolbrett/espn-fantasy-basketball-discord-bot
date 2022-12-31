import discord
from discord import option, application_command
from discord.ext import commands
from LeagueData import LeagueData
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

league_data = LeagueData(os.getenv('LEAGUE_ID_BBL'), 2023)
guild_id = os.getenv('GUILD_ID_BBL')

#get guild ID by right-clicking on server icon then hit Copy ID
@bot.slash_command(name="hey", guild_ids=[guild_id])
@option(
    "hey", 
    str, 
    description="Brett"
)
async def hey(interaction):
    await interaction.response.send_message("Hello!")

@bot.command(name="three-weeks", description="Grab past three weeks totals", guild=discord.Object(id=guild_id))
async def three_weeks(interaction: discord.Interaction):
    await interaction.response.send_message("three-weeks")


"""
@bot.command()
async def hey(ctx, *args):
    print(args)
    await ctx.response.send_message("Hey")
"""

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

"""
@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if message.content.startswith('$roast'):
        array = message.content.split()
        if len(array) > 1:
            name = str(array[1])
            await message.channel.send(name + ' smells like shit')
        else:
            await message.channel.send("Usage: `$roast [name]`")

    if message.content.startswith('$set-year'):
        array = message.content.split()
        if len(array) > 1:
            league_data.set_year(int(array[1]))
            await message.channel.send("League Year set to: " + str(league_data.league.year))
        else:
            usage = bot.commands['$set-year']
            await message.channel.send(usage)

    if message.content.startswith('$three-weeks'):
        array = message.content.split()
        result = ""
        if len(array) > 1:
            week = int(array[1])
            result += "*Showing data from week " + str(week) + " of year " + str(league_data.league.year) + "*\n"
            result += league_data.three_weeks_total_as_string(week=week)
        else:
            result += "*Showing data from current week of year " + str(league_data.league.year) + "*\n"
            result += league_data.three_weeks_total_as_string(0)
        await message.channel.send(result)
    
    if message.content.startswith('$help'):
        result = "Below are commands I support:\n"
        result += "\n`[command] | [how to use]`"
        for command, usage in bot.commands.items():
            result += "\n|\n`" + command + " | " + usage + "`"
        await message.channel.send(result)
    
    if message.content.startswith('$standings'):
        result = league_data.old_get_standings_as_string()
        await message.channel.send(result)
"""
bot.run(os.getenv('BOT_TOKEN'))