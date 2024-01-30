import streamlit as st
import pandas as pd
import numpy as np
import module
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="EPA",
    page_icon="🏈",
)

"""
# EPA in run game

This page shows the EPA ranking for running offenses and defenses against the run.

"""

data_path = "data/"
plays_df = pd.read_csv(os.path.join(data_path, 'plays.csv'))

teams_list = module.get_all_home_teams(data_path)

off_epa = {team:module.get_offensive_epa_run(plays_df, team) for team in teams_list}

pd.DataFrame(off_epa)
