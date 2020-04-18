import requests
import json
from getpass import getpass
import functools

# Base URLs
FPL_URL = "https://draft.premierleague.com/api/"
LOGIN_URL = "https://users.premierleague.com/accounts/login/"

# Login Details - Fill these in
USERNAME = '' 
PASSWORD =  getpass()
LEAGUE_ID = ''

payload = {
    'login':USERNAME,
    'password':PASSWORD,
    'redirect_uri': 'https://fantasy.premierleague.com/',
    'app':'plfpl-web'
}

s = requests.Session()
try:
    s.post(LOGIN_URL, data=payload)
except:
    print("Failed to login")


def getPlayersLiveInfo(event_num):
    r = s.get(FPL_URL + 'event/' + str(event_num) + '/live')
    live_info = r.json()
    return live_info['elements']


def getLivePointsForTeam(entry_id, event_num, live_player_info):
    r = s.get(FPL_URL + 'entry/' + str(entry_id) + '/event/' + str(event_num))
    team = r.json()['picks'][:11]
    live_points = 0
    for player in team:
        player_live = live_player_info.get(str(player['element']))
        live_points += player_live['stats']['total_points']
    return(live_points)  


def getLiveLeagueTable():
    r = s.get(FPL_URL + 'league/' + LEAGUE_ID + '/details')
    league_details = r.json()
    league = []
    
    r = s.get(FPL_URL + 'game')
    event_num = r.json()['current_event']
    
    live_player_info = getPlayersLiveInfo(event_num)
    
    for player in league_details['standings']:
        entry = [x for x in league_details['league_entries'] if x['id'] == player['league_entry']][0]
        
        live_points = getLivePointsForTeam(entry['entry_id'], event_num, live_player_info)
        res = {
            "rank": player['rank'],
            "team": entry['entry_name'],
            "player": entry['player_first_name'] + ' ' + entry['player_last_name'],
            "live_points": player['total'] + (live_points - player['event_total']),
            "total_points": player['total'],
            "weekly_score": live_points
        }
        league.append(res)
    league.sort(key=lambda x: x.get('live_points'), reverse=True)
    return league


def getTeamsData():
    r = s.get(FPL_URL + 'league/' + LEAGUE_ID + '/details')
    league_details = r.json()

    teams_history = []

    for player in league_details['standings']:
        entry = [x for x in league_details['league_entries'] if x['id'] == player['league_entry']][0]
        entry_id = entry['entry_id']

        r = s.get(FPL_URL + 'entry/' + str(entry_id) + '/history')

        team_history = []
        team_history_total = []

        for gw in r.json()['history']:
            team_history.append(gw['points'])
            team_history_total.append(gw['total_points'])

        teams_history.append({
            "player": entry['player_first_name'] + ' ' + entry['player_last_name'],
            "entry_id": entry['entry_id'],
            "history": team_history,
            "history_total": team_history_total
        })

    return teams_history


@functools.lru_cache(maxsize=1024)
def getPlayer(id):
    r = s.get(FPL_URL + 'bootstrap-static')
    event_data = r.json()

    players = event_data['elements']
    player = [x['web_name'] for x in players if x['id'] == id][0]
    return player


@functools.lru_cache(maxsize=1024)
def getOwner(id):
    r = s.get(FPL_URL + LEAGUE_ID + '/element-status')
    players = r.json()['element_status']
    owner_id = [x['owner'] for x in players if x['element'] == id]

    if len(owner_id) == 0 or None in owner_id:
        return {"short_name": "--", "name": "Unowned"}
    else:
        owner_id = owner_id[0]

    r = s.get(FPL_URL + LEAGUE_ID + '/details')
    leagues = r.json()['league_entries']
    owner = [{"short_name": x['short_name'], "name": x['player_first_name'] + ' ' + x['player_last_name']} 
            for x in leagues if x['entry_id'] == owner_id][0]

    return owner


def getFixtures(id):
    r = s.get(FPL_URL + 'event/' + id +  '/fixtures')
    fixtures = r.json()

    r = s.get(FPL_URL + 'bootstrap-static')
    event_data = r.json()

    for index, fixture in enumerate(fixtures):
        home_id = fixture['team_h']
        away_id = fixture['team_a']

        teams = event_data['teams']

        fixture['team_h'] = [x['name'] for x in teams if x['id'] == home_id][0]
        fixture['team_a'] = [x['name'] for x in teams if x['id'] == away_id][0]
        
        for i, stat in enumerate(fixture['stats']):
            for j, home_stat in enumerate(stat['h']):
                player = home_stat['element']
                home_stat['name'] = getPlayer(player)
                home_stat['owner'] = getOwner(player)
                stat['h'][j] = home_stat

            for j, away_stat in enumerate(stat['a']):
                player = away_stat['element']
                away_stat['name'] = getPlayer(player)
                away_stat['owner'] = getOwner(player)
                stat['a'][j] = away_stat

            fixture['stats'][i] = stat
            

        fixtures[index] = fixture
    
    return fixtures

def getCurrent():
    r = s.get(FPL_URL + 'bootstrap-static')
    event_data = r.json()

    return event_data['events']['current']