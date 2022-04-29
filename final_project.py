# Final Project, SI 507
# Author: Mike VerHulst
#

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import seaborn as sns
import matplotlib.pyplot as plt
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

### testing getting player info

##getting a Sidney Crosby's info
# sid_results = utils.getPlayer('Sidney Crosby')
# sid = sid_results[0]
# sid_stats = utils.player_stats(sid)
# # testing playerToClass
# sid_crosby = utils.playerToClass(sid)

## getting a Alexander Ovechkin's info
# ovi_results = utils.getPlayer('Alexander Ovechkin')
# ovi = ovi_results[0]
# ovi_stats = utils.player_stats(ovi)
# # testing playerToClass
# ovechkin = utils.playerToClass(ovi)

### plotting Crosby vs Ovechkin
# utils.plotGoalAssists(sid_crosby, ovechkin)
# utils.plotAll(sid_crosby, ovechkin)

### testing players with different playing career timelines
# seider_results = utils.getPlayer('Moritz Seider')
# seider = seider_results[0]
# seider_stats = utils.player_stats(seider)
# # testing playerToClass
# seider = utils.playerToClass(seider)

# utils.plotAll(ovechkin, seider)

players = input('Please enter the names of two players you would like to compare seperated by a comma \n(Sidney Crosby, Alexander Ovechkin): ')
p1, p2 = players.split(',')

p1_results = utils.getPlayer(p1)
p2_results = utils.getPlayer(p2)

p1_tag = p1_results[0]
p2_tag = p2_results[0]

p1_skater = utils.playerToClass(p1_results[0])
p2_skater = utils.playerToClass(p2_results[0])

utils.plotAll(p1_skater,p2_skater)