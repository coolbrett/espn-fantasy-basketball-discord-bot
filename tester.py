from LeagueData import LeagueData

"""
This file is just a tester file. Used to easily test out some code before 
putting it into other(more important) files
"""

def main():
    league_data = LeagueData(121940, 2023)
    #temp = get_standings(league_data=league_data)
    #scoreboard(league_data=league_data)
    #get_draft_recap(league_data=league_data)
    #get_abbreviations(league_data=league_data)
    #get_top_scorer(league_data=league_data)
    #get_box_scores_and_matchups_of_week(league_data=league_data, week=11)
    #league_data.league.scoreboard(matchupPeriod=1)
    return

def get_standings(league_data: LeagueData) -> dict:
    """Grabs sorted list of standings, and splits the teams into their divisions"""
    teams = league_data.league.standings()
    #each key is division and value is a list of teams
    teams_by_division = dict()

    for team in teams:
        if team.division_name in teams_by_division:
            teams_by_division[team.division_name] += [team] 
        else:
            teams_by_division.__setitem__(team.division_name, [team])
  
    #print(str(teams_by_division.keys()))
    #print(str(teams_by_division['East']))

    return teams_by_division


def get_draft_recap(league_data: LeagueData) -> dict:
    """Gets draft recap and turns into a dictionary where keys are the round numbers, 
        and values are the list of Pick objects in that round"""

    picks_by_round = dict()

    for pick in league_data.league.draft:
        if pick.round_num in picks_by_round:
            picks_by_round[pick.round_num] += [pick]
        else:
            picks_by_round.__setitem__(pick.round_num, [pick])
    
    return picks_by_round

def get_abbreviations(league_data: LeagueData) -> dict:
    """Gets all abbreviations of teams in the league and their corresponding team name"""
    abbrev = dict()

    for team in league_data.league.teams:
        abbrev.__setitem__(team.abbrev, team.team_name)

    return abbrev

def get_history(league_data: LeagueData) -> list:
    """Gets Final Standings of league"""
    return league_data.league.standings()

def get_top_scorer(league_data: LeagueData):
    """Gets top fantasy point scorer from a list of Box Player objects"""

    for box in league_data.league.box_scores(2):
        h_lineup = box.home_lineup
        a_lineup = box.away_lineup

        h_lineup.sort(key=lambda player: player.points, reverse=True)

        for player in h_lineup:
            print(player)
        
        break

def get_box_scores_and_matchups_of_week(league_data: LeagueData, week: int) -> list:
        """Grabs list of box scores and matchups of week given, and returns a list of dictionaries
            containing the matchups and their corresponding box scores"""
        box_scores = league_data.league.box_scores(matchup_period=week)
        matchups = league_data.league.scoreboard(matchupPeriod=week)
        data = []
        count = 0
        for matchup in matchups:
            #print(str(matchup))
            #print(box_scores[count].home_team.team_name)
            #print(box_scores[count].away_team.team_name)
            data.append({matchup: box_scores[count]})
            #print(str(data))
            count += 1
        #print(str(data))
        return data
        

main()