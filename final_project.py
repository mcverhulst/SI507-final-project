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

# getting rosters for all active teams
# teams_rosters = []
# for team in teams:
#     team_id = team['id']
#     teams_rosters.append(requests.get(f"{base_url}teams/{team_id}?expand=team.roster&season=20212022").json()['teams'][0])

# writing team data with rosters to json for future reference
# utils.write_json('20212022_rosters.json' , teams_rosters)

teams = pd.read_json('20212022_rosters.json')
print(teams.iloc[1]['roster']['roster'][4])
print(teams.iloc[1]['roster']['roster'][4]['position']['code'])
print(type(teams))
# teams.to_csv('derpington.csv')



# defining classes for skaters and goalies
class skater():
    def __init__(self, fName, lName, position, goals, assists, points, games, dict):
        self.fname = dict['person']['fullname'],
        self.lName = lName,
        self.position = dict['position']['code'],
        self.goals = goals,
        self.assists = assists,
        self.points = points,
        self.games = games
        # self.fname = fName,
        # self.lName = lName,
        # self.position = position,
        # self.goals = goals,
        # self.assists = assists,
        # self.points = points,
        # self.games = games

    def points(self):
        return self.points

    def goals(self):
        return self.goals

    def assists(self):
        return self.assists

    def points(self):
        return self.assists

    def games(self):
        return self.games

    def position(self):
        return self.position

class goalie(skater):
    def __init__(self, fName, lName, position, goals, assists, points, games, \
            saves, gaa, svPct, wins, loss, shutOut):
        super().__init__(fName, lName, position, goals, assists, points, games)
        self.saves = saves,
        self.gaa = gaa,
        self.svPCT = svPct,
        self.wins = wins,
        self.loss = loss,
        self.shutOut = shutOut,

# test_skater = skater(teams.iloc[1]['roster']['roster'][0])
# test_goalie = goalie(teams.iloc[1]['roster']['roster'][4])

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
utils.write_json('final_tree.json', json_str)