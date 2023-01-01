from FBBot import FBBot
from LeagueData import LeagueData
import discord

def main():
    league_data = LeagueData(121940, 2023)
    #get_standings(league_data=league_data)
    #scoreboard(league_data=league_data)
    return

def get_standings(league_data: LeagueData):
    """Built this to format into a discord message -- looks like dog shit on mobile"""
    result = ""
    result += str("**Team**").ljust(32, " ") + str("**W**") + str("**L**").rjust(5, " ") + str("**Division**").rjust(12, " ") + "\n"
    result += str("").ljust(25, '-') + "-".rjust(8, " ") + "-".rjust(5, " ") + "--------".rjust(12, " ") + "\n"
    for team in league_data.league.standings():
        result += str(team.team_name).ljust(32, " ") + str(team.wins) + str(team.losses).rjust(5, " ") + str(team.division_name).rjust(10, " ") + "\n"
    #print(result)
    return result

def scoreboard(league_data: LeagueData):
    temp = league_data.league.scoreboard(0)
    print(str(temp))

main()