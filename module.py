import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import os

def create_football_field(linenumbers=True,
                          endzones=True,
                          highlight_line=False,
                          highlight_line_number=50,
                          highlighted_name='Line of Scrimmage',
                          fifty_is_los=False,
                          figsize=(12, 6.33)):
    """
    Function that plots the football field for viewing plays.
    Allows for showing or hiding endzones.
    """
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1,
                             edgecolor='r', facecolor='lime', zorder=0)


    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='black')
    if fifty_is_los:
        plt.plot([60, 60], [0, 53.3], color='blue')
        plt.text(62, 50, '<- Player Yardline at Snap', color='blue')
    # Endzones
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='black',
                                alpha=0.2,
                                zorder=0)
        ez2 = patches.Rectangle((110, 0), 120, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='black',
                                alpha=0.2,
                                zorder=0)
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    plt.xlim(0, 120)
    plt.ylim(-5, 58.3)
    plt.axis('off')
    if linenumbers:
        for x in range(20, 110, 10):
            numb = x
            if x > 50:
                numb = 120 - x
            plt.text(x, 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='black')
            plt.text(x - 0.95, 53.3 - 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='black', rotation=180)
    if endzones:
        hash_range = range(11, 110)
    else:
        hash_range = range(1, 120)

    for x in hash_range:
        ax.plot([x, x], [0.4, 0.7], color='black')
        ax.plot([x, x], [53.0, 52.5], color='black')
        ax.plot([x, x], [22.91, 23.57], color='black')
        ax.plot([x, x], [29.73, 30.39], color='black')

    if highlight_line:
        hl = highlight_line_number + 10
        plt.plot([hl, hl], [0, 53.3], color='blue')
        plt.text(hl + 2, 50, '<- {}'.format(highlighted_name),
                 color='blue')
    return fig, ax

def get_positions_from_player_in_game(data_path, player_name, gameId):
    """
        Returns dataframe with all x and y positions of the given
        in the given game.
    """
    for i in range(1,10):
        tracking_df = pd.read_csv(os.path.join(data_path, "tracking_week_"+str(i)+".csv"))
        gameIds = tracking_df["gameId"].unique()
        if gameId in gameIds: # check if the wanted game is in this week's games
            players = tracking_df[(tracking_df["gameId"]==gameId)]["displayName"].unique()
            if player_name in players:
                player_tracks = tracking_df[(tracking_df["gameId"]==gameId) & (tracking_df["displayName"]==player_name)]
                return player_tracks[["playId","x","y"]]
            else:
                raise IndexError("Player " +str(player_name)+" not found in game "+str(gameId))
    raise IndexError("Game with gameId: "+str(gameId)+" not found")

def obtain_gameId(data_path, home_team, visitor_team):
    games_df = pd.read_csv(os.path.join(data_path, "games.csv"))
    try:
        res = games_df[(games_df['homeTeamAbbr'] == home_team) & (games_df['visitorTeamAbbr'] == visitor_team)].gameId.values[0]
    except IndexError:
        return -1
    return res

def draw_positions_from_player_in_game(data_path, player_name, homeTeam, visitorTeam):
    gameId = obtain_gameId(data_path, homeTeam, visitorTeam)
    all_positions = get_positions_from_player_in_game(data_path, player_name, gameId)
    x_marks = np.arange(0,120,.5)
    y_marks = np.arange(0,53.3,.5)
    field_matrix = np.zeros((len(x_marks), len(y_marks)))
    for _, position in all_positions.iterrows():
        try:
            field_matrix[int(np.floor(position["x"]*2)),int(np.floor(position["y"]*2))] += 1
        except IndexError:
            continue
    field_matrix = field_matrix/field_matrix.sum()
    fig, ax = create_football_field()
    fig.set_facecolor('None')
    ax.imshow(field_matrix.T, cmap="summer", origin="lower", extent=[-0.1,119.9,-0.1,53,2], alpha=.5, vmax=1e-10)
    return fig

def get_all_home_teams(data_path):
    games_df = pd.read_csv(os.path.join(data_path, "games.csv"))
    return games_df["homeTeamAbbr"].unique().tolist()

def get_all_away_teams_given_home_team(data_path, home_team):
    games_df = pd.read_csv(os.path.join(data_path, "games.csv"))
    return games_df[games_df["homeTeamAbbr"]==home_team]["visitorTeamAbbr"].unique().tolist()

def get_all_player_names_given_game(data_path, home_team, visitor_team):
    gameId = obtain_gameId(data_path, home_team, visitor_team)
    for i in range(1,10):
        tracking_df = pd.read_csv(os.path.join(data_path, "tracking_week_"+str(i)+".csv"))
        gameIds = tracking_df["gameId"].unique()
        if gameId in gameIds: # check if the wanted game is in this week's games
            players_ids = tracking_df[(tracking_df["gameId"]==gameId)]["nflId"].dropna().unique() # the football will return nan, we drop it
            break
    players_ls = []
    players_df = pd.read_csv(os.path.join(data_path, 'players.csv'))
    for id in players_ids:
        player_details = players_df[players_df['nflId']==id][['displayName', 'position']]
        players_ls.append(player_details['displayName'].values[0] + ' ('+player_details['position'].values[0]+')')
    return players_ls

def get_offensive_epa_run(plays_df, team):
    plays = plays_df[plays_df['possessionTeam']==team].dropna(subset=["expectedPointsAdded"])
    epa_run, count_run, epa_des_run, count_des_run, epa_scramble, count_scramble = 0, 0, 0, 0, 0, 0
    for _, play in plays.iterrows():
        pass_result = play['passResult']
        epa = play['expectedPointsAdded']
        if pass_result=='R':
            epa_scramble += epa
            count_scramble +=1
        if pass_result!=pass_result:
            epa_des_run += epa
            count_des_run +=1
        epa_run += epa
        count_run +=1
    return epa_run/count_run, epa_des_run/count_des_run, epa_scramble/count_scramble