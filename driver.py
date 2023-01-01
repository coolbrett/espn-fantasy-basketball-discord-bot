import discord
from discord import commands as discord_commands
from discord.ext import commands as discord_ext_commands
from LeagueData import LeagueData
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

intents = discord.Intents.all()
bot = discord.Bot()
bot.intents.all()

league_data = LeagueData(os.getenv('LEAGUE_ID_BBL'), 2023)
guild_id = os.getenv('GUILD_ID_BBL')

#get guild ID by right-clicking on server icon then hit Copy ID
@bot.command(name="hey", description="Say Hey to LeBot!", guild_ids=[guild_id])
async def hey(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@bot.command(name="three-weeks", description="Grabs three week totals for each team from the week number given and sends a sorted list", guild_ids=[guild_id])
#Would like to add descriptions to parameter but do not know how
async def three_weeks(interaction: discord.Interaction, week: int):
    result = ""
    result += "*Showing data from week {} of year {}*\n".format(week, league_data.league.year)
    result += league_data.three_weeks_total_as_string(week=week)
    await interaction.response.send_message(result)


@bot.command(name="scoreboard", description="Grab scoreboard from current week or provide a week number", guild_ids=[guild_id])
async def scoreboard(interaction: discord.Interaction, week: int=None):
    #would like to get team logos on scoreboard one day
    if week == None: 
        week = league_data.find_current_week()
    
    matchups = league_data.league.scoreboard(week)
    embed = discord.Embed(title=str(league_data.league.year - 1)+ "-" + str(league_data.league.year) + " Week " + str(week) + " Scoreboard")
    for matchup in matchups:
        score = str(matchup.away_team.team_name) + " `" + str(int(matchup.away_final_score)) + "` | `" + str(int(matchup.home_final_score)) + "` " + str(matchup.home_team.team_name)
        #away_record = str(matchup.away_team.wins) + "-" + str(matchup.away_team.losses) + "-" + str(matchup.away_team.ties)
        #description = str(away_record).ljust(40, " ") + "hey"
        description = "".ljust(64, "-")
        embed.add_field(name=score, value=description, inline=False)

    await interaction.response.send_message(embed=embed)


@bot.command(name="standings", description="Current Standings for Fantasy League", guild_ids=[guild_id])
async def standings(interaction: discord.Interaction):
    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Standings")
    return

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

"""
@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if message.content.startswith('$set-year'):
        array = message.content.split()
        if len(array) > 1:
            league_data.set_year(int(array[1]))
            await message.channel.send("League Year set to: " + str(league_data.league.year))
        else:
            usage = bot.commands['$set-year']
            await message.channel.send(usage)
"""
bot.run(os.getenv('BOT_TOKEN'))