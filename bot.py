import discord
from discord.ext import commands
from discord import app_commands
from LeagueData import LeagueData
import os
from dotenv import load_dotenv
from pathlib import Path
import espn_api
from functools import wraps
from FirebaseData import FirebaseData
from logger_config import logger


"""
This is the main file of the discord bot. All commands are being written here.

@github coolbrett
"""
# All sensitive data needs to be held and imported in the .env file
# the .env has to be loaded first before being used
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

intents = discord.Intents.default()
intents.guilds = True  # Ensures your bot can track server events
intents.guild_messages = True
intents.message_content = True  # Required if you're handling message events
bot = commands.Bot(command_prefix="/", intents=intents)


# global league data object for commands to access FBB league data
league_data: LeagueData = None

firebase_data = FirebaseData()

#get all guild_id's
guild_ids = firebase_data.get_all_guild_ids()

def generate_league_data():
    """Decorator to run pre-command logic for commands requiring guild_id and league_id."""
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: discord.Interaction, *args, **kwargs):
            await interaction.response.defer()
            logger.info(f"Command received from {interaction.user.name}: {interaction.command.name}")

            # Skip pre-command logic for DMs or commands without a guild context
            if interaction.guild_id is None:
                return await func(interaction, *args, **kwargs)

            # Global league data access
            global league_data
            guild_id_as_string = str(interaction.guild_id)

            # Check if the guild is in Firebase
            if guild_id_as_string in guild_ids:
                guild_fb = firebase_data.get_guild_information(guild_id_as_string)

                # Check if the guild exists in Firebase and has credentials
                if guild_fb is None or 'credentials' not in guild_fb or 'league_id' not in guild_fb['credentials']:
                    await interaction.followup.send(
                        "Your league is not set up! Use /setup to configure your league credentials."
                    )
                    return


                league_id = guild_fb['credentials']['league_id']

                # Create league with or without private credentials
                if 'espn_s2' in guild_fb['credentials'] and 'swid' in guild_fb['credentials']:
                    espn_s2 = guild_fb['credentials']['espn_s2']
                    swid = guild_fb['credentials']['swid']
                    league_data = await create_league_data(
                        interaction=interaction, league_id=league_id, espn_s2=espn_s2, swid=swid
                    )
                else:
                    league_data = await create_league_data(
                        interaction=interaction, league_id=league_id, espn_s2=None, swid=None
                    )
            
            # Execute the original command
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator

async def create_league_data(interaction: discord.Interaction, league_id, espn_s2, swid):
        """Helper function to handle creation of LeagueData"""
        try:
            #specifying 2025 as year because it is the most recent year
            data = LeagueData(league_id=int(league_id), year=2025, espn_s2=espn_s2, swid=swid)
            return data
        except espn_api.requests.espn_requests.ESPNInvalidLeague:
            await interaction.followup.send("League credentials are invalid, use /setup again with correct credentials")


@bot.tree.command(name="hey", description="Say Hey to LeBot!", )
async def hey(interaction: discord.Interaction):
    await interaction.followup.send("Hello!", ephemeral=True)


@bot.tree.command(name="three-weeks",
             description="Grabs three week totals for each team from the week number given and sends a sorted list",
             )
@app_commands.describe(week="Ex: 5 will get totals from weeks 3, 4, and 5")
@generate_league_data()
async def three_weeks(interaction: discord.Interaction, week: int = None):

    if week is None:
        week = league_data.find_current_week()
    
    current_year = league_data.league.year
    previous_year = current_year - 1
    previous_weeks = [week - 2, week - 1, week]
    totals = league_data.three_weeks_total_as_string(week=week)

    embed = discord.Embed(title="")
    embed.add_field(name=f"Past three weeks' totals from weeks {previous_weeks[0]}, {previous_weeks[1]}, {previous_weeks[2]} of {previous_year}-{current_year}", value=totals)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="standings", description="Current Standings for Fantasy League", )
@app_commands.describe(year="Year to get data from (current year is default)")
@generate_league_data()
async def standings(interaction: discord.Interaction, year: int = None):
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
            description += "`" + str(place) + ")   " + team.team_abbrev.ljust(5) + "   {}-{}-{}".format(team.wins, team.losses, team.ties).ljust(9) + "`\n"
            place += 1
        embed.add_field(name=str(div), value=description, inline=False)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="draft-recap", description="Get Draft Recap from current or previous season", )
@app_commands.describe(
    year="Year to get data from (defaults to current year)",
    round="Specific round to get (gets all rounds by default)"
)
@generate_league_data()
async def draft_recap(interaction: discord.Interaction, year: int = None, round: int = None):

    def check_year_validity(year: int): 
        if year < 2017 or year > 2024:
            return False
        return True

    original_year = league_data.league.year
    if year is not None:
        if check_year_validity(year=year):
            league_data.set_year(year=year)
        else:
            await interaction.followup.send("Year given is invalid, try again with a year that your league existed in")
            return

    embed = discord.Embed(
        title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year) + " Draft Recap")
    
    try:
        draft_recap = league_data.get_draft_recap()
    except espn_api.requests.espn_requests.ESPNInvalidLeague:
        await interaction.followup.send(f"Your league did not exist in {league_data.league.year}, try a more recent year :)")
        return

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
                    5) + "  {}".format(player_name).ljust(9) + "`\n"

            description += "\n"
            embed.add_field(name=("Round: " + str(round_num)), value=description, inline=False)
    else:
        round_list_of_picks = draft_recap[round]
        description = "`#   Team".ljust(12) + "Pick`\n"
        for pick in round_list_of_picks:
            # append pick info
            player_name = pick.playerName
            if len(player_name) > 18:
                temp = player_name.split()
                player_name = f"{temp[0][0]}. {temp[1]}"

            description += "`" + str(str(pick.round_pick) + ")").ljust(4) + pick.team.team_abbrev.ljust(
                5) + "  {}".format(player_name).ljust(9) + "`\n"

        description += "\n"
        embed.add_field(name=("Round: " + str(round)), value=description, inline=False)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="abbreviations",
             description="Gets all abbreviations of teams in the league and their corresponding team name",
             )
@app_commands.describe(year="Year to get data from (defaults to current year)")
@generate_league_data()
async def abbreviations(interaction: discord.Interaction, year: int = None):
    original_year = league_data.league.year
    if year is not None:
        league_data.set_year(year=year)

    embed = discord.Embed(title=str((league_data.league.year - 1)) + "-" + str(league_data.league.year))
    description = "`Abbrev".ljust(8) + " Team`\n"

    abbreviations = league_data.get_abbreviations()

    for abbrev, team_name in abbreviations.items():
        description += f"`{abbrev}".ljust(8) + f" {team_name}`\n"
    embed.add_field(name="Abbreviations", value=description, inline=False)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="history", description="Gets Final Standings of the league of the year given", )
@app_commands.describe(year="Year to get data from (defaults to current year)")
@generate_league_data()
async def history(interaction: discord.Interaction, year: int):
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
            description += f"`{place}) {team.team_abbrev}".ljust(10) + f" {team.wins}-{team.losses}-{team.ties}`\n"
            place += 1

    embed.add_field(name=title, value=description, inline=False)
    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(year=original_year)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="scoreboard", description="Grab scoreboard from current week or provide a week number",
             )
@app_commands.describe(
    week="Week to get data from",
    year="Year to get data from (defaults to current year)"
)
@generate_league_data()
async def scoreboard(interaction: discord.Interaction, week: int = None, year: int = None):
    # scoreboard is unable to get playoff matchups
    # Box scores cannot be used before 2019, so command breaks when going to 2018 or earlier
    # Errors out on years where the league has uneven teams -- bye weeks for some teams
    original_year = league_data.league.year
    if year is not None:
        if week is not None:
            if year < 2019:
                await interaction.followup.send("Cannot get box scores prior to 2019")
                return
            league_data.set_year(year=year)  
        else:
            await interaction.followup.send("Provide a week number if going into previous seasons!")
            return

    if week is None:
        week = league_data.find_current_week()

    embeds = []
    embed = discord.Embed(title="Week " + str(week) + " Scoreboard (" + str(league_data.league.year - 1) + "-" + str(
        league_data.league.year) + ")")
    embeds.append(embed)

    #box_scores = league_data.league.box_scores(matchup_period=week)
    box_scores = league_data.league.box_scores(matchup_period=week)


    for box_score in box_scores:
        #each box score will be an embed message
        embed = discord.Embed(title="")
        
        #checks to make sure neither team has bye
        if not box_score.away_lineup or not box_score.home_lineup:
            continue

        team_name_away = box_score.away_team.team_name
        team_name_home = box_score.home_team.team_name
        score_away = box_score.away_score
        score_home = box_score.home_score
        top_scorer_home = league_data.get_top_scorer(lineup=box_score.home_lineup)
        top_scorer_away = league_data.get_top_scorer(lineup=box_score.away_lineup)

        TEAM_ABBREV_SPACING = 6
        PLAYER_NAME_MAX = 22

        if len(top_scorer_home.name) > PLAYER_NAME_MAX:
            top_scorer_home.name = league_data.shorten_player_name(top_scorer_home.name)
        if len(top_scorer_away.name) > PLAYER_NAME_MAX:
            top_scorer_away.name = league_data.shorten_player_name(top_scorer_away.name)
        
        abbrev_away = box_score.away_team.team_abbrev
        abbrev_home = box_score.home_team.team_abbrev

        name = f"{team_name_away}"
        value = f"`{int(score_away)}`"
        embed.add_field(name=name, value=value, inline=False)

        name = f"{team_name_home}"
        value = f"`{int(score_home)}`"
        embed.add_field(name=name, value=value, inline=False)

        name = f"~~-----------------~~\n**Top Performers**"
        value = f"`{abbrev_away.ljust(TEAM_ABBREV_SPACING)}{top_scorer_away.name.ljust(PLAYER_NAME_MAX)}{int(top_scorer_away.points)}`\n`{abbrev_home.ljust(TEAM_ABBREV_SPACING)}{top_scorer_home.name.ljust(PLAYER_NAME_MAX)}{int(top_scorer_home.points)}`"
        embed.add_field(name=name, value=value, inline=False)

        embeds.append(embed)

    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)

    await interaction.followup.send(embeds=embeds)

@bot.tree.command(name="box-score", description="Grab box score for a team in any week or year",
             )
@app_commands.describe(
    team_abbreviation="Abbreviation of Team you want box score of",
    week="Week to get data from",
    year="Year to get data from (defaults to current year)"
)
@generate_league_data()
async def box_score(interaction: discord.Interaction, team_abbreviation: str, week: int = None, year: int = None):
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
    if team is None:
        await interaction.followup.send("Team abbreviation given does not exist in league, try using /abbreviations to get a list of team abbreviations in this league")
        return
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


@bot.tree.command(name="top-half-players-percentage", description="Gets the top half of all rostered players and gives percentage of how many top-half players a has", )
@app_commands.describe(
    year="Year to get data from (defaults to current year)",
    stat="Type 'avg' to sort players by average, leave blank for totals"
)
@generate_league_data()
async def top_half_players_percentage(interaction: discord.Interaction, year: int = None, stat: str = None):
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


@bot.tree.command(name="record-vs-all-teams", description="Every team's record if they played all teams every week", )
@app_commands.describe(year="Year to get data from (defaults to current year)")
@generate_league_data()
async def record_vs_all_teams(interaction: discord.Interaction, year: int = None):

    if year is None:
        year = league_data.league.year
    elif year < 2019:
        await interaction.followup.send("Box scores are unavailable prior to 2019")
        return

        
    original_year = league_data.league.year
    if year is not None:
        league_data.set_year(year=year)

    embed = discord.Embed(title=f"Record vs. All Teams {league_data.league.year - 1}-{league_data.league.year}")
    #each team ID gets a string W-L-T
    if year is None:
        year = league_data.league.year
    data = league_data.get_record_vs_all_teams()
    name = "`#".ljust(6) + "TEAM".ljust(8) + "RECORD".ljust(12) + "PERC%`"
    description = ""
    place = 1
    for team_id, record in data.items():
        team = league_data.league.get_team_data(team_id=team_id)
        description += f"`{place})".ljust(6) + f"{team.team_abbrev}".ljust(8) + f"{record['wins']}-{record['losses']}-{record['ties']}".ljust(12)
        win_percentage = league_data.get_win_percentage(wins=record['wins'], losses=record['losses'], ties=record['ties'])
        description += f"{win_percentage}`\n"
        place += 1
    embed.add_field(name=name, value=description)


    # set year back to original year if it was changed
    if league_data.league.year != original_year:
        league_data.set_year(original_year)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="setup", description="Provide ESPN Fantasy Basketball League information")
@app_commands.describe(
    fantasy_league_id="Fantasy League ID -> use /help-setup for more information",
    espn_s2="Only needed for private leagues -> use /help-setup-private for more information",
    swid="Only needed for private leagues -> use /help-private for more information"
)
async def setup(interaction: discord.Interaction, fantasy_league_id: int, espn_s2: str = None, swid: str = None):
    # Store this information where guild_id is key, and value is object containing guild_id and league credentials
    new_league_object_info = dict()
    guild_id = interaction.guild_id
    global league_data

    # Defer the response immediately to prevent timeout
    await interaction.response.defer(ephemeral=True)

    try:
        logger.info("Setup called -- Creating league in setup")
        league_data = await create_league_data(
            interaction=interaction, league_id=fantasy_league_id, espn_s2=espn_s2, swid=swid
        )

        # Add league info to the dictionary
        if espn_s2 is not None and swid is not None:
            new_league_object_info["credentials"] = {
                "league_id": str(fantasy_league_id),
                "espn_s2": str(espn_s2),
                "swid": str(swid),
            }
        else:
            new_league_object_info["credentials"] = {"league_id": str(fantasy_league_id)}

        logger.info("Sending new league object to Firebase")
        firebase_data.add_new_guild(new_league_object_info, str(guild_id))

        # Send success message
        logger.info("New league setup successful for fantasy_league_id: " + str(fantasy_league_id))
        await interaction.followup.send("Setup successful! Call `/standings` to see how your season is going!", ephemeral=True)
    except Exception as e:
        logger.error(f"Error during setup: {e}")
        await interaction.followup.send(
            "An error occurred during setup :( Make sure all parameters given are correct for your league. If setup issues persist, open an issue in GitHub here: https://github.com/coolbrett/espn-fantasy-basketball-discord-bot/issues", ephemeral=True
        )


@bot.tree.command(name="help-setup-private", description="Directions on how to get espn_s2 and swid values", )
async def help_setup_private_league(interaction: discord.Interaction):
    await interaction.followup.send("You can find these two values after logging into your ESPN Fantasy account and going to any webpage inside of your league. (Chrome Browser) Right click anywhere on the website and click inspect option. From there click Application on the top bar. On the left under Storage section click Cookies then http://fantasy.espn.com. From there you should be able to find your swid and espn_s2 variables and values. It remains the same through different sessions.")
    return

@bot.tree.command(name="help-setup", description="Directions on how to get Fantasy League ID", )
async def help_setup_public_league(interaction: discord.Interaction):
    await interaction.followup.send("MOBILE APP: Go to the `League Info` tab in your league to get the League ID\n\nWEBSITE: On any page inside the league, the league ID is specified in the URL. Should be 6 digits.")
    return

@bot.tree.command(name="report-issue", description="Details on how to report an issue", )
async def report_issue(interaction: discord.Interaction):
    await interaction.followup.send("Report or search for issues here: https://github.com/coolbrett/espn-fantasy-basketball-discord-bot/issues")

@bot.event
async def on_guild_available(guild: discord.Guild):
    #this code runs when the bot joins a server
    global guild_ids
    if str(guild.id) not in guild_ids:
        guild_ids.append(str(guild.id))
        logger.info("sending ID to firebase upon joining")
        firebase_data.add_new_guild({str(guild.id): {'guild_id': str(guild.id)}}, guild_id=guild.id)
    return

@bot.event
async def on_application_command_error(context: discord.Interaction, error):
    logger.info("In app command error")
    logger.error(error)

    if isinstance(error.original, NameError):
        logger.error(str(error.original))
        await context.interaction.followup.send("Your league has not been setup yet, or the credentials given are invalid. Use `/setup` to configure your league.")
    
    if isinstance(error.original, espn_api.requests.espn_requests.ESPNInvalidLeague):
        await context.interaction.followup.send("League credentials do not match any leagues on ESPN, or league did not exist in year given.")

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')
    
    # Sync commands globally
    await bot.tree.sync()
    logger.info("Commands have been synced globally!")
    # for guild in bot.guilds:
    #     logger.info(f'joined {guild.name}')
    return

try:
    bot.run(os.getenv('BOT_TOKEN'))
except Exception as e:
    logger.error(f"!!! An error occurred: {e}")
    
