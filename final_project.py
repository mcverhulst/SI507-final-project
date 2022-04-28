# Final Project, SI 507
# Author: Mike VerHulst
#

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import final_utils as utils

base_url = 'https://statsapi.web.nhl.com/api/v1/'

# team_id = 15
# season = "20212022"
# r = requests.get("https://statsapi.web.nhl.com/api/v1/teams/" + str(team_id) + "?expand=team.roster&season=" + season)
# team_data = r.json()

# getting a list of all active teams
teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()['teams']
# print(teams)

### getting rosters for all active teams
# teams_rosters = []
# for team in teams:
#     team_id = team['id']
#     teams_rosters.append(requests.get(f"{base_url}teams/{team_id}?expand=team.roster&season=20212022").json()['teams'][0])

### writing team data with rosters to json for future reference
# utils.write_json('20212022_rosters.json' , teams_rosters)

teams = pd.read_json('20212022_rosters.json')
# print(teams.iloc[1]['roster']['roster'][4])
# print(teams.iloc[1]['roster']['roster'][4]['position']['code'])
# print(type(teams))
# teams.to_csv('derpington.csv')

# test_skater = utils.skater(teams.iloc[1]['roster']['roster'][0])
# test_goalie = utils.goalie(teams.iloc[1]['roster']['roster'][4])


### Building the tree
tree = utils.TreeNode('Would you like to compare players or teams?')
tree.children.append(utils.TreeNode("Would you like to look at 1 team's stats or compare 2 teams?"))
child2 = utils.TreeNode("Would you like to look at 1 player or compare 2 players?")
tree.children.append(child2)
tree.children[0].children.append(utils.TreeNode('Do stuff'))
child2.children.append(utils.TreeNode('Do other stuff'))
child2.children[0].children.append(utils.TreeNode('Great Grand Kid'))

json_str = json.dumps(tree, indent=2)

### writing the tree to json
# utils.write_json('final_tree.json', json_str)


### getting a Sidney Crosby's info
sid_results = utils.getPlayer('Sidney Crosby')
sid = sid_results[0]
sid_stats = utils.player_stats(sid)
print(sid_stats.head(5))


### testing playerToClass
# print(sid.find('a').get('href'))
sid_crosby = utils.playerToClass(sid)

print(sid_crosby.goals[0].sum())
