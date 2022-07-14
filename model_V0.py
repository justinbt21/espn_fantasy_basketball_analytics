# -*- coding: utf-8 -*-
"""
Created on Sat May 21 13:35:07 2022

@author: Justin Tran
"""

import sys

sys.path.insert(0, r'C:/Users/JustinTran/Documents/Github/basketball_reference_scraper')
sys.path.insert(0, r'C:/Users/JustinTran/Documents/Github/espn_fantasy_basketball_analytics')

from espn_api.basketball.league import League
from basketball_reference_scraper.players import get_game_logs, get_player_splits
from basketball_reference_scraper.teams import get_team_ratings
from espn_fantasy_basketball_analytics.statmanager import statmanager
from espn_fantasy_basketball_analytics.nba_fantasy import teamManager
import pandas as pd
from datetime import datetime
from xgboost import XGBRegressor
from xgboost import plot_importance
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from matplotlib import pyplot
import calendar

import numpy as np

import warnings
warnings.filterwarnings('ignore')

# Pull player average, variance, opp defensive rating, home/away, lastNgames average, lastNgames variance, DoW, days rest (PTS)
# Imprvements: Look at player's frequency of shots per area and how the opposing team defends area (opp_FG%)
league = teamManager(league_id=league_id, year=year, team_name=team_name, espn_s2=espn_s2, swid=swid)
team = league.getRosterStats(team_name)


team_ratings = get_team_ratings(season_end_year=2022)

df = pd.DataFrame()
player_list = team.loc[team['MIN'].astype(float) >= 28.0]['name']
for player_name in player_list:
    player_games = get_game_logs(player_name, 2022)
    player_games['name'] = player_name
    player_games['MP'] = player_games['MP'].apply(lambda x: datetime.strptime(x, '%M:%S'))
    player_games['MP'] = player_games['MP'].apply(lambda x: round(x.minute + (x.second / 60),2))
    pts_df = player_games[['name', 'DATE', 'MP', 'PTS', 'FG', 'FGA', 'HOME/AWAY', 'OPPONENT']]
    pts_df['PTS'] = pts_df['PTS'].astype(int)
    pts_df['FG'] = pts_df['FG'].astype(int)
    pts_df['FGA'] = pts_df['FGA'].astype(int)
    pts_df['MP_avg'] = pts_df['MP'].rolling(window=82, min_periods=8, closed='left').mean()
    pts_df['MP_var'] = pts_df['MP'].rolling(window=82, min_periods=8, closed='left').var()
    pts_df['pts_avg'] = pts_df['PTS'].rolling(window=82, min_periods=8, closed='left').mean()
    pts_df['pts_var'] = pts_df['PTS'].rolling(window=82, min_periods=8, closed='left').var()
    pts_df['l7_pts_avg'] = pts_df['PTS'].rolling(window=8, min_periods=8, closed='left').mean()
    pts_df['l7_pts_var'] = pts_df['PTS'].rolling(window=8, min_periods=8, closed='left').var()
    pts_df['l7_MP_avg'] = pts_df['MP'].rolling(window=8, min_periods=8, closed='left').mean()
    pts_df['l7_MP_var'] = pts_df['MP'].rolling(window=8, min_periods=8, closed='left').var()
    pts_df['l14_pts_avg'] = pts_df['PTS'].rolling(window=8, min_periods=14, closed='left').mean()
    pts_df['l14_pts_var'] = pts_df['PTS'].rolling(window=8, min_periods=14, closed='left').var()
    pts_df['l14_MP_avg'] = pts_df['MP'].rolling(window=8, min_periods=14, closed='left').mean()
    pts_df['l14_MP_var'] = pts_df['MP'].rolling(window=8, min_periods=14, closed='left').var()
    pts_df['DoW'] = pts_df['DATE'].apply(lambda x: pd.Timestamp(x).dayofweek)
    pts_df['DoW'] = pts_df['DoW'] = pts_df['DoW'].apply(lambda x: calendar.day_name[x])
    pts_df['days_rest'] = pts_df['DATE'].diff(1).dt.days

    pts_df = pts_df.merge(team_ratings[['TEAM','DRTG/A']], left_on='OPPONENT', right_on='TEAM')
    pts_df.drop(columns='TEAM', inplace=True)
    
    pts_df
    
    df = pd.concat([df, pts_df])

df = df[~df['MP_avg'].isna()]
df.reset_index(drop=True, inplace=True)

cat_attribs = ['HOME/AWAY','DoW']
df['HOME/AWAY'] = df['HOME/AWAY'].astype('category')
df['DoW'] = df['DoW'].astype('category')

y = df['PTS']
X = df.loc[:, ~df.columns.isin(['name','PTS','DATE','OPPONENT','MP', 'FGA', 'FG', 'DoW', 'HOME/AWAY'])]
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=.2, random_state = 0)

# Define categorical columns
categorical = list(train_X.select_dtypes('category').columns)
print(f"Categorical columns are: {categorical}")

# Define numerical columns
numerical = list(train_X.select_dtypes('number').columns)
print(f"Numerical columns are: {numerical}")

# cat_pipe = Pipeline([
#     ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
#     ('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
# ])

# Define numerical pipeline
num_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])

preprocessor = ColumnTransformer([
    # ('cat', cat_pipe, categorical),
    ('num', num_pipe, numerical)
])

pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('model', XGBRegressor(n_estimators=50))
])

pipe.fit(train_X, train_y)

# cat_columns = preprocessor.named_transformers_['cat']['encoder'].get_feature_names_out(categorical)
# columns = np.append(cat_columns, numerical)

# Inspect training data before and after
# print("******************** Training data ********************")
# display(train_X)
# display(pd.DataFrame(preprocessor.transform(train_X), columns=numerical))

# # Inspect test data before and after
# print("******************** Test data ********************")
# display(test_X)
# display(pd.DataFrame(preprocessor.transform(test_X), columns=columns))

prediction = pipe.predict(test_X)

mean_absolute_error(test_y, prediction)

test_df = pd.merge(test_X, test_y, left_index=True, right_index=True)
test_df['prediction'] = prediction.tolist()
test_df = pd.merge(test_df, df[['name']], left_index=True, right_index=True)
columns = test_df.columns.tolist()[-1:] + test_df.columns.tolist()[:-1]
test_df = test_df[columns]


