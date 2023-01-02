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
        else:
            await interaction.response.send_message("Provide a week number if going into previous seasons!")
            return

    if week == None: 
        week = league_data.find_current_week()    
    
    matchups = league_data.league.scoreboard(week)
    embed = discord.Embed(title=str(league_data.league.year - 1)+ "-" + str(league_data.league.year) + " Week " + str(week) + " Scoreboard")
    for matchup in matchups:
        score = str(matchup.away_team.team_name) + " `" + str(int(matchup.away_final_score)) + "` | `" + str(int(matchup.home_final_score)) + "` " + str(matchup.home_team.team_name)
        description = "".ljust(64, "-")
        embed.add_field(name=score, value=description, inline=False)
    
    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)
    
    await interaction.response.send_message(embed=embed)


@bot.command(name="standings", description="Current Standings for Fantasy League", guild_ids=[guild_id])
async def standings(interaction: discord.Interaction, year: int=None):
    
    original_year = league_data.league.year
    if year != None:
        league_data.set_year(year=year)
    
    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Standings")
    standings = league_data.get_standings()
    for div, list_of_teams in standings.items():
        #print(str(div))
        place = 1
        description = ""
        description += "`#    Team".ljust(15) + "W-L-T`\n"
        for team in list_of_teams:
            #print(str(team))
            description += "`" + str(place) + ")   " + team.team_abbrev.ljust(5) + " |  {}-{}-{}".format(team.wins, team.losses, team.ties).ljust(9) + "`\n"
            place += 1
        embed.add_field(name=str(div), value=description, inline=False)

    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.response.send_message(embed=embed)


@bot.command(name="draft-recap", description="Get Draft Recap from current or previous season", guild_ids=[guild_id])
async def draft_recap(interaction: discord.Interaction, year: int=None, round: int=None):
    original_year = league_data.league.year
    if year != None:
        league_data.set_year(year=year)
    
    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Draft Recap")
    draft_recap = league_data.get_draft_recap()

    if round == None:
        for round_num, list_of_picks in draft_recap.items():
            #header line
            description = "`#  Team".ljust(13) + "Pick`\n"
            for pick in list_of_picks:
                #append pick info
                player_name = pick.playerName
                if len(player_name) > 18:
                    temp = player_name.split()
                    player_name = f"{temp[0][0]}. {temp[1]}"

                description += "`" + str(str(pick.round_pick) + ")").ljust(4) + pick.team.team_abbrev.ljust(5) + "|  {}".format(player_name).ljust(9) + "`\n"

            description += "\n"
            embed.add_field(name=("Round: " + str(round_num)), value=description, inline=False)
    else:
        round_list_of_picks = draft_recap[round]
        description = "`#  Team".ljust(13) + "Pick`\n"
        for pick in round_list_of_picks:
            #append pick info
            player_name = pick.playerName
            if len(player_name) > 18:
                temp = player_name.split()
                player_name = f"{temp[0][0]}. {temp[1]}"

            description += "`" + str(str(pick.round_pick) + ")").ljust(4) + pick.team.team_abbrev.ljust(5) + "|  {}".format(player_name).ljust(9) + "`\n"

        description += "\n"
        embed.add_field(name=("Round: " + str(round)), value=description, inline=False)

    
    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)
    
    await interaction.response.send_message(embed=embed)


@bot.command(name="abbreviations", description="Gets all abbreviations of teams in the league and their corresponding team name", guild_ids=[guild_id])
async def abbreviations(interaction: discord.Interaction, year: int=None):
    original_year = league_data.league.year
    if year != None:
        league_data.set_year(year=year)
    
    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year))
    description = "`Abbrev".ljust(8) + "| Team`\n"

    abbreviations = league_data.get_abbreviations()

    for abbrev, team_name in abbreviations.items():
        description += f"`{abbrev}".ljust(8) + f"| {team_name}`\n"
    embed.add_field(name="Abbreviations", value=description, inline=False)


    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.response.send_message(embed=embed)


@bot.command(name="history", description="Gets Final Standings of the league of the year given", guild_ids=[guild_id])
async def history(interaction: discord.Interaction, year: int):
    original_year = league_data.league.year
    
    if original_year == year:
        #Don't know how to tell when season is over, so current year is not available until next year starts
        await interaction.response.send_message("Cannot use /history on current season -- try /standings")
        return

    league_data.set_year(year=year)
    
    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " History")
    title = ""
    description = ""

    final_standings = league_data.get_history()
    place = 2
    for team in final_standings:
        if team.team_id == final_standings[0].team_id:
            #Champion
            title = f"Champion🏆: {team.team_name}"
        else:
            #the rest
            description += f"`{place}) {team.team_abbrev}".ljust(10) + f"| {team.wins}-{team.losses}-{team.ties}`\n"
            place += 1

    embed.add_field(name=title, value=description, inline=False)
    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)
    
    await interaction.response.send_message(embed=embed)

@bot.command(name="new_scoreboard", description="Grab scoreboard from current week or provide a week number", guild_ids=[guild_id])
async def new_scoreboard(interaction: discord.Interaction, week: int=None, year: int=None):
    #scoreboard is unable to get playoff matchups 
    original_year = league_data.league.year
    if year != None:
        if week != None:
            league_data.set_year(year=year)
        else:
            await interaction.response.send_message("Provide a week number if going into previous seasons!")
            return

    if week == None: 
        week = league_data.find_current_week()    
    
    matchups = league_data.league.scoreboard(week)
    embed = discord.Embed(title=str(league_data.league.year - 1)+ "-" + str(league_data.league.year) + " Week " + str(week) + " Scoreboard")
    for matchup in matchups:
        #each field will be team, the description will be their top scorer (and later injury rate?)
        continue
    
    #set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bot.run(os.getenv('BOT_TOKEN'))