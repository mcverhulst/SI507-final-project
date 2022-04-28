import csv
import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

class TreeNode(dict):
    def __init__(self, name, children=None):
        super().__init__()
        self.__dict__ = self
        self.name = name
        self.children = list(children) if children is not None else []

    def from_dict(dict_):
        """ Recursively (re)construct TreeNode-based tree from dictionary. """
        node = TreeNode(dict_['name'], dict_['children'])
#        node.children = [TreeNode.from_dict(child) for child in node.children]
        node.children = list(map(TreeNode.from_dict, node.children))
        return node


class skater():
    def __init__(self, name, seasons, goals, assists, points, games):
        self.name = name,
        self.seasons = seasons,
        self.goals = goals,
        self.assists = assists,
        self.points = points,
        self.games = games

    def points(self):
        return self.points

    def goals(self):
        return self.goals

    def assists(self):
        return self.assists

    def games(self):
        return self.games

    def position(self):
        return self.position


class goalie(skater):
    def __init__(self, name, seasons, goals, assists, points, games, \
            saves, gaa, svPct, wins, loss, shutOut):
        super().__init__(name, seasons, goals, assists, points, games)
        self.saves = saves,
        self.gaa = gaa,
        self.svPCT = svPct,
        self.wins = wins,
        self.loss = loss,
        self.shutOut = shutOut,


def get_nhl_data(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more NHL results to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the results.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()


def read_csv(filepath, encoding='utf-8', newline='', delimiter=','):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data


def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter=','):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

        return data


def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def getPlayer(name):
    '''
    Takes name from user and searches hokcey-reference.com for that player. If
    player is found will return the players BeautifulSoup tag that contains the
    url with that player's stats.

    Paramaeters: (str) Name of a player

    Returns:List of BeautifulSoup tags that match the search termS.
    '''
    name = name.lower().split()
    lname = name[-1]
    url = f'https://www.hockey-reference.com/players/{name[-1][0]}'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    players = soup.find_all(class_='nhl')
    tags = list(players)

    searched = []

    for i in range(len(tags)):
        x = tags[i].contents[0]
        x = str(x.contents[0]).lower()
        if lname in x:
            searched.append(tags[i])
            # return tags[i]
        else:
            continue
    if len(searched) < 1:
        print("Sorry, I didn't find that player")
    else:
        return searched


def player_stats(player):
    '''
    Input: (BeautifulSoup tag) player info
    Returns: pandas dataframe with player's stats
    '''
    url = player.find('a').get('href')

    hockey_url = f"https://www.hockey-reference.com{url}"

    page = requests.get(hockey_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find_all('table')
    df = pd.read_html(str(table))[1]
    df.columns = df.columns.get_level_values(1)

    def seasonToInt(x):
        return int(x[:4])
    df = df[:-1] # removing summary stats
    df['Season_int'] = df['Season'].apply(seasonToInt)


    return df


def playerToClass(player):
    df = player_stats(player)
    x = skater(
        name = player.find('a').contents,
        seasons = df['Season_int'].values,
        goals = df.G.values,
        assists = df.A.values,
        points = df.PTS.values,
        games = df.GP.values,
    )

    return x


def plotGoals(p1, p2):
    '''
    Input: two instances of player class
    what: goals, assits, points, games
    '''

    plt.plot(p1.seasons[0], p1.goals[0])
    plt.plot(p2.seasons[0], p2.goals[0])
    plt.xlabel('NHL Seasons')
    plt.ylabel(f"Goals Scored")
    plt.xticks(rotation=45)
    plt.show()

def plotAssists(p1, p2):
    '''
    Input: two instances of player class
    what: goals, assits, points, games
    '''

    plt.plot(p1.seasons[0], p1.goals[0])
    plt.plot(p2.seasons[0], p2.goals[0])
    plt.xlabel('NHL Seasons')
    plt.ylabel(f"Goals Scored")
    plt.xticks(rotation=45)
    plt.show()

def plotAll(p1, p2):
    # currently broken
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    ax1.scatter(p1.seasons[0], p1.goals[0])
    ax1.scatter(p2.seasons[0], p2.goals[0])
    ax1.set_title('Goals per season')

    ax2.scatter(p1.seasons[0], p1.assists[0])
    ax2.scatter(p2.seasons[0], p2.assists[0])
    ax2.set_title('Assists per season')

    ax3.scatter(p1.seasons[0], p1.points[0])
    ax3.scatter(p2.seasons[0], p2.points[0])
    ax3.set_title('Points per season')

    ax4.scatter(p1.seasons[0], p1.games, label=p1.name[0])
    ax4.scatter(p2.seasons[0], p2.games, label=p2.name[0])
    ax4.set_title('Games played per season')

    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    plt.legend()
    plt.show()

def plotGoalAssists(p1,p2):
    f, axarr = plt.subplots(2, sharex=True) # figure, axes = plt.sub....
    axarr[0].plot(p1.seasons[0], p1.goals[0]) # subplot 1
    axarr[0].plot(p2.seasons[0], p2.goals[0]) # subplot 1

    axarr[0].set_title('Sharing X axis')
    axarr[1].plot(p1.seasons[0], p1.assists[0]) # subplot 2
    axarr[1].plot(p2.seasons[0], p2.assists[0]) # subplot 2

    plt.show()

def plotPointsGames(p1,p2):
    f, axarr = plt.subplots(2, sharex=True) # figure, axes = plt.sub....
    axarr[0].plot(p1.seasons[0], p1.points[0]) # subplot 1
    axarr[0].plot(p2.seasons[0], p2.points[0]) # subplot 1

    axarr[0].set_title('Sharing X axis')
    axarr[1].plot(p1.seasons[0], p1.games[0]) # subplot 2
    axarr[1].plot(p2.seasons[0], p2.games[0]) # subplot 2

    plt.show()
