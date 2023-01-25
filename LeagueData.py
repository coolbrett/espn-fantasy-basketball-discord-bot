# Basketball API
from espn_api.basketball import *
from espn_api.basketball import box_player, box_score
import os
from dotenv import load_dotenv
from pathlib import Path
import espn_api

# All sensitive data needs to be held and imported in the .env file
# the .env has to be loaded first before being used
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

"""
Class for the data being built around the league ID and year given

@github coolbrett
"""


class LeagueData:

    def __init__(self, league_id: int, year: int, espn_s2: str = None, swid: str = None):
        """LeagueData holds data about the FBB League"""
        if espn_s2 != None and swid != None:
            self.league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        else:
            self.league = League(league_id=league_id, year=year)

    def find_current_week(self):
        """The ESPN API being used doesn't keep track of the current week in the fantasy year it is, 
            so this finds the current week and returns it"""

        # grabbing first two teams and comparing their games played just in case the first team had a bye week
        temp_team = self.league.teams[0]
        other_team = self.league.teams[1]
        num = temp_team.wins + temp_team.losses + temp_team.ties + 1
        other = other_team.wins + other_team.losses + other_team.ties + 1

        if num == other | num > other:
            return num
        else:
            return other

    def set_league(self, league_id: int, year: int, espn_s2: str = None, swid: str = None):
        """Gives ability to change leagues"""
        if espn_s2 != None and swid != None:
            self.league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        else:
            self.league = League(league_id=league_id, year=year)

    def set_year(self, year: int):
        """Set league year to a different year - ONLY WORKS FOR BBL"""
        self.league = League(league_id=self.league.league_id, year=year, espn_s2=os.getenv('ESPN_S2_BBL'),
                             swid=os.getenv('SWID_BBL'))

    def three_weeks_total_as_string(self, week: int) -> str:
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
        # list of objects
        three_weeks_list = []

        self.__get_list_team_abbreviations_for_past_three_weeks(three_weeks_list)

        for week in three_weeks_data:
            for i in range(len(three_weeks_data[week])):
                matchup = three_weeks_data[week][i]
                home_team = matchup.home_team
                away_team = matchup.away_team

                for j in range(len(three_weeks_list)):
                    if home_team.team_abbrev == three_weeks_list[j]['team_abbrev']:
                        three_weeks_list[j]['past_three_weeks_total'] += matchup.home_final_score
                    if away_team.team_abbrev == three_weeks_list[j]['team_abbrev']:
                        three_weeks_list[j]['past_three_weeks_total'] += matchup.away_final_score

        def sort_three_weeks_list(list: list):
            return list['past_three_weeks_total']

        three_weeks_list.sort(key=sort_three_weeks_list, reverse=True)
        return three_weeks_list

    def __get_list_team_names_for_past_three_weeks(self, list_to_populate):
        for team in self.league.teams:
            # print(str(team.team_name))
            list_to_populate.append({'team_name': team.team_name, 'past_three_weeks_total': 0, 'team_object': team})


    def __get_list_team_abbreviations_for_past_three_weeks(self, list_to_populate):
        """Helper method to get team abbreviations for past three weeks stat"""
        for team in self.league.teams:
            list_to_populate.append({'team_abbrev': team.team_abbrev, 'past_three_weeks_total': 0, 'team_object': team})


    def __report_three_weeks_list(self, three_weeks_list):
        """Helper method to build report for three weeks statd"""
        temp = ""
        count = 1
        temp = "`#   Team".ljust(12) + "3WT`"

        for team in three_weeks_list:
            # temp += "\n" + str(count) + ". " + str(team['team_name']) + ": **" + str(
            #     int(team['past_three_weeks_total'])) + "**"
            temp += f"\n`{count})".ljust(6) + f"{team['team_abbrev']}".ljust(7) + f"{int(team['past_three_weeks_total'])}`"
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

    def get_top_scorer(self, lineup: list) -> box_player:
        """Gets top fantasy point scorer from a list of Box Player objects"""
        lineup.sort(key=lambda player: player.points, reverse=True)
        return lineup[0]

    def get_box_score_of_matchup(self, week: int, team: Team) -> box_score:
        """Gets box score of week and Team passed in"""
        box_scores_of_week = self.league.box_scores(matchup_period=week, matchup_total=True)

        for box_score in box_scores_of_week:
            # compare team id's -- if True then return
            if box_score.away_team.team_id == team.team_id or box_score.home_team.team_id == team.team_id:
                return box_score

    def get_box_scores_and_matchups_of_week(self, week: int) -> list:
        """Grabs list of box scores and matchups of week given, and returns a list of dictionaries
            containing the matchups and their corresponding box scores"""
        # print(f"in get_box_scores_and_matchups_of_week")
        box_scores = self.league.box_scores(matchup_period=week)
        # print("got box scores")
        # print(f"Year: {self.league.year} Week: {week}")
        matchups = self.league.scoreboard(matchupPeriod=week)
        # print('got scoreboard')
        data = []
        count = 0
        for matchup in matchups:
            data.append({matchup: box_scores[count]})
            count += 1
        return data

    def shorten_player_name(self, player_name: str) -> str:
        """Shortens player name to be first inital then last name [G. Antetokounmpo]"""
        temp = player_name.split()
        return f"{temp[0][0]}. {temp[1]}"

    def find_length_of_longest_team_name(self, matchup: Matchup) -> int:
        """Returns the length of the longest team name of a given matchup"""
        num = 0

        if len(matchup.away_team.team_name) > len(matchup.home_team.team_name):
            num = len(matchup.away_team.team_name)
        else:
            num = len(matchup.home_team.team_name)

        return num
    
    def get_lineup_for_team(self, team_id: int, week: int = None, year: int = None) -> list:
        """
        Method to get a team's lineup for a given week and/or year
        """
        #return a sorted list of players by point totals
        if year is not None:
            self.set_year(year=year)
        
        if week is None:
            week = self.find_current_week()

        box_scores_of_week = self.league.box_scores(matchup_period=week)
        
        for box_score in box_scores_of_week:
            if box_score.home_team.team_id == team_id:
                box_score.home_lineup.sort(key=lambda player: player.points, reverse=True)
                return box_score.home_lineup

            if box_score.away_team.team_id == team_id:
                box_score.away_lineup.sort(key=lambda player: player.points, reverse=True)
                return box_score.away_lineup

    def get_team_by_abbreviation(self, team_abbreviation: str) -> Team:
        """
        Method to get the Team object by their corresponding team abbreviation
        """
        for team in self.league.teams:
            if team.team_abbrev.casefold() == team_abbreviation.casefold():
                return team
    
    def get_list_of_all_players_rostered(self, stat: str = None) -> list:
        """
        Iterates all team rosters and appends all players to a list, 
        then returns a sorted list by fantasy points either by 
        avg or total points (determined by stat parameter)
        """
        
        rostered_players = []
        for team in self.league.teams:
            for player in team.roster:
                rostered_players.append(player)
        
        #if-else branch here to decide to sort by totals or by avg
        if stat == "avg":
            rostered_players.sort(key=lambda player: player.avg_points, reverse=True)
        else:
            rostered_players.sort(key=lambda player: player.total_points, reverse=True)

        return rostered_players

    def get_top_half_percentage_for_each_team(self, stat: str = None) -> dict:
        """
        Gets all players on a roster as a list, sorted by either total points or average points, and 
        returns a dictionary with the keys as team_id's and the values as percentage 
        of players they have on the top half of the list
        """
        rostered_players = []
        if stat == "avg":
            rostered_players = self.get_list_of_all_players_rostered(stat=stat)
        else:
            rostered_players = self.get_list_of_all_players_rostered()

        rostered_players = rostered_players[0:int(len(rostered_players)/2)]
        top_half_player_percentages_by_team = dict()
        perc = float(1/len(rostered_players))

        for roster_player in rostered_players:
            for team in self.league.teams:
                for team_player in team.roster:
                    if team_player.playerId == roster_player.playerId:
                        if team.team_id in top_half_player_percentages_by_team.keys():
                            top_half_player_percentages_by_team[team.team_id] += perc
                        else:
                            top_half_player_percentages_by_team.__setitem__(team.team_id, perc)
        
        return top_half_player_percentages_by_team

    def get_record_vs_all_teams(self) -> dict:
        """
        Get each team's record if they played all teams every week
        """
        #does not support year parameter yet
        records = dict()
        num_of_weeks = self.find_current_week()
        full_weeks = num_of_weeks - 1
        if full_weeks != 0:
            week = 1
            while week < num_of_weeks:
                data = dict()
                #get dict with keys as team_id and values as score for the week
                #print(f"Week: {week}")
                box_scores = self.league.box_scores(matchup_period=week)
                for box_score in box_scores:
                    data.__setitem__(box_score.away_team.team_id, box_score.away_score)
                    data.__setitem__(box_score.home_team.team_id, box_score.home_score)

                #do W-L-T here
                #
                data = dict(sorted(data.items(), key=lambda team: team[1], reverse=True))
                list_of_scores = list()
                previous_team_id: int
                #account for bye weeks in reg season
                num_of_teams = len(self.league.teams)
                wins: int
                if num_of_teams % 2 == 0:
                    wins = num_of_teams - 1
                else:
                    wins = num_of_teams - 2
                losses = 0
                for team_id, score in data.items():
                    if score == 0:
                        continue
                    #print(f"{team_id}: {score}")
                    if list_of_scores.count(score) == 0:
                        list_of_scores.append(score)
                    else:
                        records[previous_team_id]['ties'] += 1
                        records[team_id]['ties'] += 1
                        previous_team_id = team_id
                        continue

                    if team_id in records:
                        records[team_id]['wins'] += wins
                        records[team_id]['losses'] += losses
                    else:
                        records.__setitem__(team_id, {'wins': wins, 'losses': losses, 'ties': 0})
                    
                    previous_team_id = team_id
                    wins -= 1
                    losses += 1
                week += 1
                #print("".ljust(20, '-'))
        records = dict(sorted(records.items(), key=lambda team: team[1]['wins'], reverse=True))
        return records

    def get_win_percentage(self, wins: int, losses: int, ties: int) -> str:
        """
        Calculates win percentage based upon parameters given, and returns the percentage to the tens place

        Ex: Win percentage: 66.6666% -> Value Returned: 66.66%
        """
        win_percentage = (wins + (ties / 2)) / (wins + losses + ties) * 100
        return str(round(win_percentage, 2))
  