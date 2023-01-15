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
    #get_list_of_all_players_rostered(league_data=league_data)
    get_top_half_percentage_for_each_team(league_data=league_data)
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
        
def get_list_of_all_players_rostered(league_data: LeagueData) -> list:
    """Iterates all team rosters and appends all players to a list, then returns a sorted list by season fantasy points total"""
    #bring in parameter to decide if you sort by total or avg
    rostered_players = []

    for team in league_data.league.teams:
        for player in team.roster:
            rostered_players.append(player)
    
    rostered_players.sort(key=lambda player: player.avg_points, reverse=True)
    """
    count = 1
    for player in rostered_players:
        print(f"{count}) {player.name} -- Total: {player.total_points}")
        count += 1
    """
    return rostered_players

def get_top_half_percentage_for_each_team(league_data: LeagueData):
    rostered_players = get_list_of_all_players_rostered(league_data=league_data)
    rostered_players = rostered_players[0:int(len(rostered_players)/2)]
    top_half_player_percentages_by_team = dict()
    perc = float(1/len(rostered_players))

    for roster_player in rostered_players:
        for team in league_data.league.teams:
            for team_player in team.roster:
                if team_player.playerId == roster_player.playerId:
                    #print(f"roster_player: {roster_player.name}\t\t{roster_player.avg_points}")
                    if team.team_id in top_half_player_percentages_by_team.keys():
                        top_half_player_percentages_by_team[team.team_id] += perc
                    else:
                        top_half_player_percentages_by_team.__setitem__(team.team_id, perc)

    
    # total = 0
    # for team_id, perc in top_half_player_percentages_by_team.items():
    #     team = league_data.league.get_team_data(team_id=team_id)
    #     perc = float("%.3f" % perc)
    #     total += perc
    #     percantage = perc * 100
    #     percantage = float("%.3f" % percantage)
    #     print(f"{team.team_abbrev}:\t\t{percantage}%")
    # print(f"total: {total}")

main()