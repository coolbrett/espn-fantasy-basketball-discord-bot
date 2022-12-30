# Basketball API
from espn_api.basketball import *

"""
Class for the data being built around fantasy league ID and year given

@version 1.0 (12/28/2022)
@github coolbrett
"""
class LeagueData:

    def __init__(self, league_id: int, year: int):
        """Initializer for LeagueData object"""
        self.league = League(league_id=league_id, year=year)

    def set_league(self, league_id: int, year: int):
        """Gives ability to change leagues"""
        self.league = League(league_id=league_id, year=year)

    def set_year(self, year: int):
        """Set league year to a different year"""
        self.league = League(league_id=self.league.league_id, year=year)

    def three_weeks_total_as_string(self, week: int):
        """Builds and prints a sorted list of teams and their three week totals"""
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
    
    def old_get_standings_as_string(self):
        result = ""
        result += str("Team").ljust(32, " ") + str("W") + str("L").rjust(5, " ") + str("Division").rjust(12, " ") + "\n"
        result += str("").ljust(25, '-') + "-".rjust(8, " ") + "-".rjust(5, " ") + "--------".rjust(12, " ") + "\n"
        for team in self.league.standings():
            result += str(team.team_name).ljust(32, " ") + str(team.wins) + str(team.losses).rjust(5, " ") + str(team.division_name).rjust(10, " ") + "\n"
        print(result)
        return result
    
    def get_standings_as_string(self):
        result = ""
        result += str("brett")
        return result
