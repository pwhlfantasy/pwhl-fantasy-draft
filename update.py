import json
from datetime import date

from pwhl_pbp_scraper import scrape_game


def update_players_in_game(game,player_points,scoring=None):
    if scoring is None:
        print("No update: no scoring configuration")
    game_date = game['game_date'].iloc[0]
    all_players_in_game = set(list(game['event_primary_player_name'].unique())+list(game['event_secondary_player_name'].unique()))#+list(game['event_tertiary_player_name'].unique())
    game_players_scores = {player:0 for player in all_players_in_game}
    for event_details in game.to_dict(orient='records'):
        event_type = event_details['event']
        if event_type=='goal':
            game_players_scores[event_details['event_primary_player_name']]+=scoring['goal']
            game_players_scores[event_details['event_secondary_player_name']]+=scoring['assist']
            if event_details['is_power_play'] or event_details['is_short_handed']:
                game_players_scores[event_details['event_primary_player_name']]+=scoring['special point']
                game_players_scores[event_details['event_secondary_player_name']]+=scoring['special point']
            # player_points[event_details['event_tertiary_player_name']]+=scoring['assist']
        elif event_type=='shot':
            if event_details['shot_quality']=="Quality on net":
                game_players_scores[event_details['event_primary_player_name']]+=scoring['shot']
        elif event_type in ['hit','blocked_shot']:
            game_players_scores[event_details['event_primary_player_name']]+=scoring[event_type]
    for player in game_players_scores:
        if player in player_points['points']:
            player_points['points'][player][game_date] = game_players_scores[player]
        else:
            player_points['points'][player] = {game_date:game_players_scores[player]}
    return player_points

def update_players(scoring = None, game_ids = None):
    if scoring is None:
        scoring = {
            'goal':2,
            'assist':1,
            'shot':0.1,
            'hit':0.1,
            'blocked_shot':0.5,
            'special point':0.5
        }
    if game_ids is None:
        game_ids = range(1,300)

    current_date = date.today()
    current_date_string =current_date.isoformat()

    try:
        with open('playerPoints.json','r') as file:
            player_points = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        player_points = {"points":{}}
        
    if "lastGameID" in player_points:
        last_updated_game = player_points["lastGameID"]
    else:
        last_updated_game = 0
    
    for game_id in game_ids:
        if game_id >last_updated_game:
            try:
                game = scrape_game(game_id)
                if game is not None and 'end_of_game' in game['event'].unique():
                    player_points = update_players_in_game(game,player_points,scoring=scoring)
                    last_updated_game = game_id
            except Exception as e:
                print(e)
    player_points['lastGameID'] = last_updated_game

    with open('playerPoints.json','w') as file:
        json.dump(player_points,file)
    return

def get_matchup_weeks_to_update(last_completed_week,current_date_string,matchup_calendar):
    matchup_week = last_completed_week
    weeks_to_update = []
    matchup_week+=1
    while current_date_string not in matchup_calendar[str(matchup_week)]['week']:
        weeks_to_update.append(str(matchup_week))
        matchup_week+=1
    weeks_to_update.append(str(matchup_week))
    return weeks_to_update

def calculate_roster_score(team_id,dates_in_matchup,teams,player_points):
    roster = teams[str(team_id)]['roster']
    score = 0
    for player in roster:
        if player in player_points["points"]:
            for date in dates_in_matchup:
                if date in player_points["points"][player]:
                    score+=player_points["points"][player][date]
        else:
            print(f"No player {player}")
    return score

def update_matchup_scores():
    with open('playerPoints.json','r') as file:
        player_points = json.load(file)
    with open('matchupScores.json','r') as file:
        matchup_scores = json.load(file)
    with open('matchupCalendar.json','r') as file:
        matchup_calendar = json.load(file)
    with open('teams.json','r') as file:
        teams = json.load(file)
    
    current_date = date.today()
    current_date_string =current_date.isoformat()
    
    if 'lastCompletedWeek' in matchup_scores:
        last_completed_week = matchup_scores['lastCompletedWeek']
    else:
        last_completed_week = -1
    
    weeks_to_update = get_matchup_weeks_to_update(last_completed_week,current_date_string,matchup_calendar)

    for week in weeks_to_update:
        new_scores = []
        for pair in matchup_scores[week]:
            pair_scores = {}
            for team_id in pair:
                pair_scores[team_id] = calculate_roster_score(team_id,matchup_calendar[week]['week'],teams,player_points)
            new_scores.append(pair_scores)
        matchup_scores[week]=new_scores
    with open('matchupScores.json','w') as file:
        json.dump(matchup_scores,file)
    return 

def update_everything(scoring = None, game_ids = None):
    update_players(scoring = scoring, game_ids = game_ids)
    update_matchup_scores()

if __name__=="__main__":
    # update_players(game_ids=range(20,30))
    update_everything(game_ids=range(30,50))