Data for each player is collected from hockey-reference.com in the form of an html table. That table is then loaded into a pandas dataframe for easier manipulation. The raw table has a two-level index for the columns that is first collapsed into a single level that makes parsing the data much easier for the players.

Once a dataframe with that player’s data is created, it is then used when creating an instance of a custom class called “skater.” Since the player’s name is not present in the table, this class combines the player’s name and their statistics in one place. This class contains the following attributes that are then used when visualizing the data:
* player.goals
* player.assists
* player.points
* player.games
* Player.name
