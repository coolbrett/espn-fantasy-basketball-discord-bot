import discord
from discord.ext import commands

from LeagueData import LeagueData
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import espn_api

"""
This is the main file of the discord bot. All commands are being written here.

@github coolbrett
"""
# All sensitive data needs to be held and imported in the .env file
# the .env has to be loaded first before being used
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# boilerplate discord code, idk what it does
intents = discord.Intents.all()
bot = discord.Bot()
bot.intents.all()

# This is where the data being used in commands is built
#league_data = LeagueData(int(os.getenv('LEAGUE_ID_BBL')), 2023)
league_data = 0

# get guild ID by right-clicking on server icon then hit Copy ID
def __build_list_of_guild_ids():
    #get all guild_id's and their data
    data = list()
    with open('fantasy_leagues.json') as json_file:
        data = json.load(json_file)
    
    temp = []
    for key in data.keys():
        temp.append(key)
    return temp

#get all guild_id's
guild_ids = __build_list_of_guild_ids()


#this runs code upon every command received
@bot.before_invoke
async def before_each_command(context: discord.ApplicationContext):
    accessible_commands = ["hey", "setup", "help-setup", "help-setup-private"]
    if context.command.name not in accessible_commands:
        global league_data
        #load league data through guild_id in context
        if str(context.guild_id) in guild_ids:
            
            data = dict()
            with open('fantasy_leagues.json') as json_file:
                data = json.load(json_file)

            if data[str(context.guild_id)] == None:
                await context.interaction.followup.send("Your league is not set up! Use /setup to configure your league credentials")
                print(context.command.name)
                return

            guild_id_as_string = str(context.guild_id)
            league_id = data[guild_id_as_string]['fantasy_league_id']
            
            #create league with and without private credentials
            if 'espn_s2' in data[guild_id_as_string] and 'swid' in data[guild_id_as_string]:
                print("has private creds")
                espn_s2 = data[guild_id_as_string]['espn_s2']
                # temp = {'espn_s2': data[guild_id_as_string]['espn_s2']}
                # data.update(temp)
                # swid = data[guild_id_as_string]['swid']
                swid = {'swid': data[guild_id_as_string]['swid']}
                # data.update(temp)
                league_data = await create_league_data(interaction=context.interaction, league_id=league_id, espn_s2=espn_s2, swid=swid)
            else:
                league_data = await create_league_data(interaction=context.interaction, league_id=league_id, espn_s2=None, swid=None)
        
async def create_league_data(interaction: discord.Interaction, league_id, espn_s2, swid):
    """Helper function to handle creation of LeagueData"""
    try:
        return LeagueData(league_id=int(league_id), year=2023, espn_s2=espn_s2, swid=swid)
    except espn_api.requests.espn_requests.ESPNInvalidLeague:
        await interaction.response.send_message("League credentials are invalid, use /setup again with correct credentials")


@bot.command(name="hey", description="Say Hey to LeBot!", guild_ids=guild_ids)
async def hey(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@bot.command(name="three-weeks",
             description="Grabs three week totals for each team from the week number given and sends a sorted list",
             guild_ids=guild_ids)
@discord.option(name="week", description="Ex: 5 will get totals from weeks 3, 4, and 5")
async def three_weeks(interaction: discord.Interaction, week: int = None):
    await interaction.response.defer()

    if week is None:
        week = league_data.find_current_week()
    
    embed = discord.Embed(title="")
    embed.add_field(name=f"Past three weeks' totals from weeks {week - 2}, {week - 1}, {week} of {league_data.league.year - 1}-{league_data.league.year}", value=league_data.three_weeks_total_as_string(week=week))
    await interaction.followup.send(embed=embed)


@bot.command(name="standings", description="Current Standings for Fantasy League", guild_ids=guild_ids)
@discord.option(name="year", description="Year to get data from (current year is default)")
async def standings(interaction: discord.Interaction, year: int = None):
    await interaction.response.defer()
    original_year = league_data.league.year
    if year != None:
        league_data.set_year(year=year)

    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Standings")
    standings = league_data.get_standings()
    for div, list_of_teams in standings.items():
        place = 1
        description = ""
        description += "`#    Team".ljust(15) + "W-L-T`\n"
        for team in list_of_teams:
            description += "`" + str(place) + ")   " + team.team_abbrev.ljust(5) + " |  {}-{}-{}".format(team.wins, team.losses, team.ties).ljust(9) + "`\n"
            place += 1
        embed.add_field(name=str(div), value=description, inline=False)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.command(name="draft-recap", description="Get Draft Recap from current or previous season", guild_ids=guild_ids)
@discord.option(name="year", description="Year to get data from (defaults to current year)")
@discord.option(name="round", description="Specific round to get (gets all rounds by default)")
async def draft_recap(interaction: discord.Interaction, year: int = None, round: int = None):
    await interaction.response.defer()
    original_year = league_data.league.year
    if year is not None:
        league_data.set_year(year=year)

    embed = discord.Embed(
        title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Draft Recap")
    draft_recap = league_data.get_draft_recap()

    if round is None:
        for round_num, list_of_picks in draft_recap.items():
            # header line
            description = "`#  Team".ljust(13) + "Pick`\n"
            for pick in list_of_picks:
                # append pick info
                player_name = pick.playerName
                if len(player_name) > 18:
                    player_name = league_data.shorten_player_name(player_name=player_name)

                description += "`" + str(str(pick.round_pick) + ")").ljust(4) + pick.team.team_abbrev.ljust(
                    5) + "|  {}".format(player_name).ljust(9) + "`\n"

            description += "\n"
            embed.add_field(name=("Round: " + str(round_num)), value=description, inline=False)
    else:
        round_list_of_picks = draft_recap[round]
        description = "`#  Team".ljust(13) + "Pick`\n"
        for pick in round_list_of_picks:
            # append pick info
            player_name = pick.playerName
            if len(player_name) > 18:
                temp = player_name.split()
                player_name = f"{temp[0][0]}. {temp[1]}"

            description += "`" + str(str(pick.round_pick) + ")").ljust(4) + pick.team.team_abbrev.ljust(
                5) + "|  {}".format(player_name).ljust(9) + "`\n"

        description += "\n"
        embed.add_field(name=("Round: " + str(round)), value=description, inline=False)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.command(name="abbreviations",
             description="Gets all abbreviations of teams in the league and their corresponding team name",
             guild_ids=guild_ids)
@discord.option(name="year", description="Year to get data from (defaults to current year)")
async def abbreviations(interaction: discord.Interaction, year: int = None):
    await interaction.response.defer()
    original_year = league_data.league.year
    if year is not None:
        league_data.set_year(year=year)

    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year))
    description = "`Abbrev".ljust(8) + "| Team`\n"

    abbreviations = league_data.get_abbreviations()

    for abbrev, team_name in abbreviations.items():
        description += f"`{abbrev}".ljust(8) + f"| {team_name}`\n"
    embed.add_field(name="Abbreviations", value=description, inline=False)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.command(name="history", description="Gets Final Standings of the league of the year given", guild_ids=guild_ids)
@discord.option(name="year", description="Year to get data from (defaults to current year)")
async def history(interaction: discord.Interaction, year: int):
    await interaction.response.defer()
    original_year = league_data.league.year
    if original_year == year:
        # Don't know how to tell when season is over, so current year is not available until next year starts
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
            # Champion
            title = f"Champion🏆: {team.team_name}"
        else:
            # the rest
            description += f"`{place}) {team.team_abbrev}".ljust(10) + f"| {team.wins}-{team.losses}-{team.ties}`\n"
            place += 1

    embed.add_field(name=title, value=description, inline=False)
    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.command(name="scoreboard", description="Grab scoreboard from current week or provide a week number",
             guild_ids=guild_ids)
@discord.option(name="week", description="Week to get data from")
@discord.option(name="year", description="Year to get data from (defaults to current year)")
async def scoreboard(interaction: discord.Interaction, week: int = None, year: int = None):
    # scoreboard is unable to get playoff matchups
    # Box scores cannot be used before 2019, so command breaks when going to 2018 or earlier
    # Errors out on years where the league has uneven teams -- bye weeks for some teams
    await interaction.response.defer()
    original_year = league_data.league.year
    if year is not None:
        if week is not None:
            league_data.set_year(year=year)
            if year < 2019:
                # Build scoreboard for years 2018 and earlier
                embeds = []
                embed = discord.Embed(title="Week " + str(week) + " Scoreboard (" + str(league_data.league.year - 1) + "-" + str(league_data.league.year) + ")")
                embeds.append(embed)
                matchups = league_data.league.scoreboard(matchupPeriod=week)

                for matchup in matchups:
                    pad_amount = league_data.find_length_of_longest_team_name(matchup=matchup) + 10
                    embed = discord.Embed(title="")
                    embed.add_field(name="".ljust(pad_amount,
                                          "-") + f"\n{matchup.away_team.team_name}:" + f" {int(matchup.away_final_score)}\n",
                            value=f"**{matchup.away_team.wins}-{matchup.away_team.losses}-{matchup.away_team.ties}**\n\n", inline=False)
                    embed.add_field(name=f"{matchup.home_team.team_name}:" + f" {int(matchup.home_final_score)}\n",
                            value=f"**{matchup.home_team.wins}-{matchup.home_team.losses}-{matchup.home_team.ties}**\n**" + "".ljust(pad_amount, "-") + "**", inline=False)
                    embeds.append(embed)

                # set year back to original year if it was changed
                if league_data.league.year != original_year:
                    league_data.set_year(original_year)

                await interaction.followup.send(embeds=embeds)
                return
        else:
            await interaction.followup.send("Provide a week number if going into previous seasons!")
            return

    if week is None:
        week = league_data.find_current_week()

    # embedded messages can only have 25 fields, so multiple embedded messages are needed just in case a league
    # has more than 12 teams
    embeds = []
    embed = discord.Embed(title="Week " + str(week) + " Scoreboard (" + str(league_data.league.year - 1) + "-" + str(
        league_data.league.year) + ")")
    embeds.append(embed)
    list_of_matchup_dicts = league_data.get_box_scores_and_matchups_of_week(week=week)

    for data in list_of_matchup_dicts:
        for matchup, box_score in data.items():

            top_scorer_home = league_data.get_top_scorer(lineup=box_score.home_lineup)
            top_scorer_away = league_data.get_top_scorer(lineup=box_score.away_lineup)

            # Top performer field goes off the side on the app :/
            embed = discord.Embed(title="")
            if len(top_scorer_away.name) > 18:
                top_scorer_away.name = league_data.shorten_player_name(player_name=top_scorer_away.name)
            elif len(top_scorer_home.name) > 18:
                top_scorer_home.name = league_data.shorten_player_name(player_name=top_scorer_home.name)

            pad_amount = league_data.find_length_of_longest_team_name(matchup=matchup) + 10
            embed.add_field(name="".ljust(pad_amount,
                                          "-") + f"\n{matchup.away_team.team_name}:" + f" {int(matchup.away_final_score)}\n",
                            value=f"**{matchup.away_team.wins}-{matchup.away_team.losses}-{matchup.away_team.ties}**\n\n__**Top Performer**__\n{top_scorer_away.name}: " + str(
                                int(top_scorer_away.points)) + "\n|", inline=False)
            embed.add_field(name=f"{matchup.home_team.team_name}:" + f" {int(matchup.home_final_score)}\n",
                            value=f"**{matchup.home_team.wins}-{matchup.home_team.losses}-{matchup.home_team.ties}**\n\n__**Top Performer**__\n{top_scorer_home.name}: " + str(
                                int(top_scorer_home.points)) + "\n**" + "".ljust(pad_amount, "-") + "**", inline=False)
            embeds.append(embed)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)

    await interaction.followup.send(embeds=embeds)

@bot.command(name="box-score", description="Grab box score for a team in any week or year",
             guild_ids=guild_ids)
@discord.option(name="team_abbreviation", description="Abbreviation of Team you want box score of")
@discord.option(name="week", description="Week to get data from")
@discord.option(name="year", description="Year to get data from (defaults to current year)")
async def box_score(interaction: discord.Interaction, team_abbreviation: str, week: int = None, year: int = None):
    await interaction.response.defer()
    original_year = league_data.league.year
    if year is not None:
        if week is not None:
            league_data.set_year(year=year)
        else:
            await interaction.followup.send("Enter a week number if going into previous seasons!")
            return
    else:
        year = original_year
    
    if year < 2019:
        await interaction.followup.send("Box score cannot be used prior to 2019")
        return
    
    if week is None:
        week = league_data.find_current_week()
    
    
    #main logic
    team = league_data.get_team_by_abbreviation(team_abbreviation=team_abbreviation)
    team_lineup = league_data.get_lineup_for_team(team_id=team.team_id, week=week, year=year)
    embed = discord.Embed(title=f"Week {week} ({year}) Breakdown")
    description = "`NAME".ljust(24) + "PTS`\n"
    
    #loop and append player name and totals to description
    for player in team_lineup:
        name = player.name
        if len(name) > 18:
            name = league_data.shorten_player_name(player_name=player.name)
        description += f"`{name}".ljust(24) + f"{int(player.points)}`\n"
    embed.add_field(name=f"{team.team_name}", value=description)
    
    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)

    await interaction.followup.send(embed=embed)


@bot.command(name="top-half-players-percentage", description="Gets the top half of all rostered players and gives percentage of how many top-half players a thas", guild_ids=guild_ids)
@discord.option(name="year", description="Year to get data from (defaults to current year)")
@discord.option(name="stat", description="type 'avg' to sort players by average, leave blank for totals")
async def top_half_players_percentage(interaction: discord.Interaction, year: int = None, stat: str = None):
    await interaction.response.defer()
    original_year = league_data.league.year
    if year is not None:
        league_data.set_year(year=year)
    
    top_half_players = {}
    if stat == "avg":
        top_half_players = league_data.get_top_half_percentage_for_each_team(stat=stat)
    else:
        top_half_players = league_data.get_top_half_percentage_for_each_team()
    
    embed = discord.Embed(title=f"Top Half of Rostered Players %")
    description = "`TEAM".ljust(8) + "PERC%`\n"
    for team_id, percentage in top_half_players.items():
        team = league_data.league.get_team_data(team_id=team_id)
        percentage = float("%.1f" % (percentage * 100))
        description += f"`{team.team_abbrev}".ljust(8) + f"{percentage}%`\n"
    embed.add_field(name="", value=description)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)
    
    await interaction.followup.send(embed=embed)


@bot.command(name="record-vs-all-teams", description="Every team's record if they played all teams every week", guild_ids=guild_ids)
@discord.option(name="year", description="Year to get data from (defaults to current year)")
async def record_vs_all_teams(interaction: discord.Interaction, year: int = None):
    await interaction.response.defer()    
    if year < 2019:
        await interaction.followup.send("Box scores are unavailable prior to 2019")
        return
        
    original_year = league_data.league.year
    if year is not None:
        league_data.set_year(year=year)

    embed = discord.Embed(title=f"Record vs. All Teams")
    #each team ID gets a string W-L-T
    if year is None:
        year = league_data.league.year
    await interaction.response.defer()
    data = league_data.get_record_vs_all_teams()
    name = "`TEAM".ljust(8) + "RECORD".ljust(12) + "PERC%`"
    description = ""
    for team_id, record in data.items():
        team = league_data.league.get_team_data(team_id=team_id)
        description += f"`{team.team_abbrev}".ljust(8) + f"{record['wins']}-{record['losses']}-{record['ties']}".ljust(12)
        win_percentage = league_data.get_win_percentage(wins=record['wins'], losses=record['losses'], ties=record['ties'])
        description += f"{win_percentage}`\n"
    embed.add_field(name=name, value=description)


    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)
    
    await interaction.followup.send(embed=embed)

@bot.command(name="setup", description="Provide ESPN Fantasy Basketball League information", guild_ids=guild_ids)
@discord.option(name="fantasy_league_id", description="Fantasy League ID -> use /help-setup for more information")
@discord.option(name="espn_s2", description="Only needed for private leagues -> use /help-setup-private for more information")
@discord.option(name="swid", description="Only needed for private leagues -> use /help-private for more information")
async def setup(interaction: discord.Interaction, fantasy_league_id: int, espn_s2: str = None, swid: str = None):
    #store this information where guild_id is key, and value is object containing guild_id and league credentials
    await interaction.response.defer()
    new_league_object_info = dict()
    guild_id = interaction.guild_id
    global league_data
    print("before league creation")
    league_data = create_league_data(interaction=interaction, league_id=fantasy_league_id, espn_s2=espn_s2, swid=swid)

    #add league info to dict
    if espn_s2 != None and swid != None:
        new_league_object_info.__setitem__(str(guild_id), {'guild_id': str(guild_id), 'fantasy_league_id': str(fantasy_league_id), 'espn_s2': str(espn_s2), 'swid': str(swid)})
    else:
        new_league_object_info.__setitem__(str(guild_id), {'guild_id': str(guild_id), 'fantasy_league_id': str(fantasy_league_id)})
    
    #load json into dict, and use update to set new info or overwrite existing data
    data = dict()
    with open('fantasy_leagues.json') as json_file:
        data = json.load(json_file)
        data.update(new_league_object_info)
        print(f"in setup\n{new_league_object_info}")

    with open('fantasy_leagues.json', 'w') as json_file:
        print(f"data dumped: {data}")
        json.dump(data, json_file)    
    
    await interaction.followup.send("Setup successful!")
    return

@bot.command(name="help-setup-private", description="Directions on how to get espn_s2 and swid values", guild_ids=guild_ids)
async def help_setup_private_league(interaction: discord.Interaction):
    await interaction.response.send_message("You can find these two values after logging into your ESPN Fantasy account and going to any webpage inside of your league. (Chrome Browser) Right click anywhere on the website and click inspect option. From there click Application on the top bar. On the left under Storage section click Cookies then http://fantasy.espn.com. From there you should be able to find your swid and espn_s2 variables and values. It remains the same through different sessions.")
    return

@bot.command(name="help-setup", description="Directions on how to get Fantasy League ID", guild_ids=guild_ids)
async def help_setup_private_league(interaction: discord.Interaction):
    await interaction.response.send_message("MOBILE APP: Go to the `League Info` tab in your league to get the League ID\n\nWEBSITE: On any page inside the league, the league ID is specified in the URL. Should be 6 digits.")
    return


@bot.event
async def on_guild_available(guild: discord.Guild):
    #this code runs when the bot joins a server
    print(f"joined {guild.id}")
    global guild_ids
    if str(guild.id) not in guild_ids:
        guild_ids.append(str(guild.id))
        print(guild_ids)
        print(guild.id)
        
        data = dict()
        with open('fantasy_leagues.json') as json_file:
            data = json.load(json_file)
        
        #add new guild id to the json with None as value
        data.update({str(guild.id): None})

        with open('fantasy_leagues.json', 'w') as json_file:
            json.dump(data, json_file)
    return

@bot.event
async def on_application_command_error(context: discord.ApplicationContext, error):
    print("In app command error")
    print(error)

    if isinstance(error.original, NameError):
        print(str(error.original))
        await context.interaction.response.send_message("Your league has not been setup yet, or the credentials given are invalid. Use `/setup` to configure your league.")
    
    if isinstance(error, espn_api.requests.espn_requests.ESPNInvalidLeague):
        await context.interaction.response.send_message("League credentials do not match any leagues on ESPN. Re-run /setup with correct credentials.")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


bot.run(os.getenv('BOT_TOKEN'))
