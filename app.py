import streamlit as st
import pandas as pd
import numpy as np
import module
import matplotlib.pyplot as plt

"""
# NFL Data Analytics

### Path of any player in any game

"""

# Add a selectbox to the sidebar:

data_path = "data/"

teams_list = module.get_all_home_teams(data_path)
home_team = st.sidebar.selectbox(
    'What is the Home Team?',
    teams_list
)

possible_away_teams = module.get_all_away_teams_given_home_team(data_path, home_team)
visitor_team = st.sidebar.selectbox(
    'What is the Visitor Team?',
    possible_away_teams
)

possible_players = module.get_all_player_names_given_game(data_path, home_team, visitor_team)
player_name = st.sidebar.selectbox(
    'What is the name of the player?',
    possible_players
)

player_name = player_name.rsplit(' ', 1)[0] # to delete position from the string

data_path = "data/"
fig = module.draw_positions_from_player_in_game(data_path, player_name, home_team, visitor_team)
fig