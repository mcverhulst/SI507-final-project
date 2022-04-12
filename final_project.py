# Final Project, SI 507
# Author: Mike VerHulst
# 

import requests
import pandas as pd
import final_utils as utils

base_url = 'https://statsapi.web.nhl.com/api/v1/'

# team_id = 15
# season = "20212022"
# r = requests.get("https://statsapi.web.nhl.com/api/v1/teams/" + str(team_id) + "?expand=team.roster&season=" + season)
# team_data = r.json()

# getting a list of all active teams
teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()['teams']
# print(teams)

# getting rosters for all active teams
teams_rosters = []
for team in teams:
    team_id = team['id']
    teams_rosters.append(requests.get(f"{base_url}teams/{team_id}?expand=team.roster&season=20212022").json()['teams'][0])

# writing team data with rosters to json for future reference
utils.write_json('20212022_rosters.json' , teams_rosters)