import discord
from LeagueData import LeagueData
from FBBot import FBBot
import os
from dotenv import load_dotenv
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
league_data = LeagueData(121940, 2023)
bot = FBBot()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
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
        result = league_data.get_standings_as_string()
        await message.channel.send(result)


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
client.run(os.getenv('BOT_TOKEN'))
