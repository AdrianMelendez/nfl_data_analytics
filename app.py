import streamlit as st
import pandas as pd
import numpy as np
import module
import matplotlib.pyplot as plt

"""
# NFL Data Analytics

## Path of any player in any game

"""

# Add a selectbox to the sidebar:
home_team = st.sidebar.selectbox(
    'What is the Home Team?',
    ('BUF', 'ARI', 'LA')
)

visitor_team = st.sidebar.selectbox(
    'What is the Visitor Team?',
    ('WAS', 'LA', 'BUF')
)

player_name = st.sidebar.selectbox(
    'What is the name of the player?',
    ('Kyler Murray', 'Byron Murphy Jr.', 'Josh Allen')
)



data_path = "data/"
fig = module.draw_positions_from_player_in_game(data_path, player_name, home_team, visitor_team)
fig