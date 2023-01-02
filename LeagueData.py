# Basketball API
from espn_api.basketball import *
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

"""
Class for the data being built around fantasy league ID and year given

@version 1.0 (12/28/2022)
@github coolbrett
"""
class LeagueData:

    def __init__(self, league_id: int, year: int):
        """Initializer for LeagueData object"""
        self.league = League(league_id=league_id, year=year, espn_s2=os.getenv('ESPN_S2_BBL'), swid=os.getenv('SWID_BBL'))

    def find_current_week(self):
        """The ESPN API being used doesn't keep track of the current week in the fantasy year it is, 
            so this finds the current week and returns it"""
        
        #grabbing first two teams and comparing their games played just in case the first team had a bye week
        temp_team = self.league.teams[0]
        other_team = self.league.teams[1]
        num = temp_team.wins + temp_team.losses + temp_team.ties + 1
        other = other_team.wins + other_team.losses + other_team.ties + 1

        if num == other | num > other:
            return num
        else:
            return other

    def set_league(self, league_id: int, year: int):
        """Gives ability to change leagues"""
        self.league = League(league_id=league_id, year=year, espn_s2=os.getenv('ESPN_S2_BBL'), swid=os.getenv('SWID_BBL'))

    def set_year(self, year: int):
        """Set league year to a different year"""
        self.league = League(league_id=self.league.league_id, year=year, espn_s2=os.getenv('ESPN_S2_BBL'), swid=os.getenv('SWID_BBL'))

    def three_weeks_total_as_string(self, week: int):
        """Builds and returns a string that is a sorted list of teams and their three week totals"""
        data = self.__get_last_three_weeks_data(week)
        three_weeks_list = self.__build_list_three_weeks_data(data)
        return self.__report_three_weeks_list(three_weeks_list)

    def __get_last_three_weeks_data(self, week: int):
        """Helper method to get the three weeks data"""
        three_weeks_data = {'current_week': self.league.scoreboard(week), 
                        'previous_week': self.league.scoreboard(week - 1), 
                        'two_weeks_back': self.league.scoreboard(week - 2)}
        return three_weeks_data
    
    def __build_list_three_weeks_data(self, three_weeks_data: dict):
        """Helper method to build the list"""
        #list of objects
        three_weeks_list = []

        self.__get_list_team_names_for_past_three_weeks(three_weeks_list)

        for week in three_weeks_data:
            for i in range(len(three_weeks_data[week])): 
                matchup = three_weeks_data[week][i]
                home_team = matchup.home_team
                away_team = matchup.away_team
                
                for j in range(len(three_weeks_list)):
                    if home_team.team_name == three_weeks_list[j]['team_name']:
                        three_weeks_list[j]['past_three_weeks_total'] += matchup.home_final_score
                    if away_team.team_name == three_weeks_list[j]['team_name']:
                        three_weeks_list[j]['past_three_weeks_total'] += matchup.away_final_score
        
        def sort_three_weeks_list(list: list):
            return list['past_three_weeks_total']

        three_weeks_list.sort(key=sort_three_weeks_list, reverse=True)
        return three_weeks_list

    def __get_list_team_names_for_past_three_weeks(self, list_to_populate):
        for team in self.league.teams:
            #print(str(team.team_name))
            list_to_populate.append({'team_name': team.team_name, 'past_three_weeks_total': 0, 'team_object': team})
        

    def __report_three_weeks_list(self, three_weeks_list):
        temp = ""
        count = 1
        for team in three_weeks_list:
            temp += "\n" + str(count) + ". " + str(team['team_name']) + ": **" + str(int(team['past_three_weeks_total'])) + "**"
            count += 1
        return temp

    def get_standings(self) -> dict:
        """Grabs sorted list of standings, and splits the teams into their divisions
        || Each key is a division and value is a list of teams"""
        teams = self.league.standings()
        teams_by_division = dict()

        for team in teams:
            if team.division_name in teams_by_division:
                teams_by_division[team.division_name] += [team] 
            else:
                teams_by_division.__setitem__(team.division_name, [team])

        return teams_by_division
    
    def get_draft_recap(self) -> dict:
        """Gets draft recap and turns into a dictionary where keys are the round numbers, 
            and values are the list of Pick objects in that round"""

        picks_by_round = dict()

        for pick in self.league.draft:
            if pick.round_num in picks_by_round:
                picks_by_round[pick.round_num] += [pick]
            else:
                picks_by_round.__setitem__(pick.round_num, [pick])
        
        return picks_by_round
    
    def get_abbreviations(self) -> dict:
        """Gets all abbreviations of teams in the league and their corresponding team name"""
        abbrev = dict()

        for team in self.league.teams:
            abbrev.__setitem__(team.team_abbrev, team.team_name)

        return abbrev
    
    def get_history(self) -> list:
        """Gets standings of league as a sorted list of teams by final record"""
        return self.league.standings()
