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
async def three_weeks(interaction: discord.Interaction, week: int=None):
    
    if week == None:
        week = league_data.find_current_week()
    
    result = ""
    result += "*Showing data from week {} of year {}*\n".format(week, league_data.league.year)
    result += league_data.three_weeks_total_as_string(week=week)
    await interaction.response.send_message(result)


@bot.command(name="scoreboard", description="Grab scoreboard from current week or provide a week number", guild_ids=[guild_id])
async def scoreboard(interaction: discord.Interaction, week: int=None, year: int=None):
    #scoreboard is unable to get playoff matchups 
    original_year = league_data.league.year
    if year != None:
        if week != None:
            league_data.set_year(year=year)
            print("League year set to: " + str(league_data.league.year))
        else:
            await interaction.response.send_message("Provide a week number if going into previous seasons!")
            return

    if week == None: 
        week = league_data.find_current_week()
        print("Week set to: " + str(week))
    
    print("Week is: {}".format(week))
    
    matchups = league_data.league.scoreboard(week)
    embed = discord.Embed(title=str(league_data.league.year - 1)+ "-" + str(league_data.league.year) + " Week " + str(week) + " Scoreboard")
    for matchup in matchups:
        score = str(matchup.away_team.team_name) + " `" + str(int(matchup.away_final_score)) + "` | `" + str(int(matchup.home_final_score)) + "` " + str(matchup.home_team.team_name)
        #away_record = str(matchup.away_team.wins) + "-" + str(matchup.away_team.losses) + "-" + str(matchup.away_team.ties)
        description = "".ljust(64, "-")
        embed.add_field(name=score, value=description, inline=False)
    
    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)
        print("League year reset to: " + str(league_data.league.year))
    print("League year: {}, week: {}\nDONE\n".format(league_data.league.year, league_data.find_current_week()))
    
    await interaction.response.send_message(embed=embed)


@bot.command(name="standings", description="Current Standings for Fantasy League", guild_ids=[guild_id])
async def standings(interaction: discord.Interaction, year: int=None):
    
    original_year = league_data.league.year
    if year != None:
        league_data.set_year(year=year)

    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Standings")
    standings = league_data.get_standings()
    #iterate through each division and add a field for each division and the description needs to be the teams W-L and other things
    for div, list_of_teams in standings.items():
        #print(str(div))
        place = 1
        description = ""
        description += "`#     Team".ljust(38) + "W-L-T`\n"
        for team in list_of_teams:
            #print(str(team))
            description += "`" + str(place) + ")     " + team.team_name.strip().ljust(25) + " |  {}-{}-{}".format(team.wins, team.losses, team.ties).ljust(9) + "`\n"
            place += 1
        embed.add_field(name=str(div), value=description, inline=False)

    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bot.run(os.getenv('BOT_TOKEN'))