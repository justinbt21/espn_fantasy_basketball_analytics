#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 14:22:32 2022

@author: JT
"""
import sys

sys.path.insert(0, r'../Github/basketball_reference_scraper')
sys.path.insert(0, r'C:/Users/JustinTran/Documents/Github/basketball_analytics')
sys.path.insert(0, r'C:/Users/JustinTran/Documents/Github/espn_fantasy_basketball_analytics')

from basketball_reference_scraper.players import get_game_logs, get_player_splits
from basketball_reference_scraper.teams import get_team_ratings
from basketball_reference_scraper.box_scores import get_box_scores
from espn_fantasy_basketball_analytics.statmanager import statmanager
from espn_fantasy_basketball_analytics.teamManager import teamManager
import pandas as pd
from datetime import datetime
import numpy as np
import calendar
import warnings

warnings.filterwarnings('ignore')

def getFeatures(player_name):
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
    pts_df['L7_pts_avg'] = pts_df['PTS'].rolling(window=8, min_periods=8, closed='left').mean()
    pts_df['L7_pts_var'] = pts_df['PTS'].rolling(window=8, min_periods=8, closed='left').var()
    pts_df['L7_MP_avg'] = pts_df['MP'].rolling(window=8, min_periods=8, closed='left').mean()
    pts_df['L7_MP_var'] = pts_df['MP'].rolling(window=8, min_periods=8, closed='left').var()
    pts_df['DoW'] = pts_df['DATE'].apply(lambda x: pd.Timestamp(x).dayofweek)
    pts_df['DoW'] = pts_df['DoW'] = pts_df['DoW'].apply(lambda x: calendar.day_name[x])
    pts_df['days_rest'] = pts_df['DATE'].diff(1).dt.days
    
    pts_df['usage'] = 
    
    
    
    pts_df = pts_df.merge(team_ratings[['TEAM','DRTG/A']], left_on='OPPONENT', right_on='TEAM')
    pts_df.drop(columns='TEAM', inplace=True)
    
    df = pts_df.reset_index(drop=True)
    
    
    return df


def getLastNTotals(games_df, date, last_n_games=1):
    
    date_df = games_df[['DATE','TEAM','OPPONENT']]
    
    date_df = filterByLastNGames(date_df, last_n_games=last_n_games)
    
    # Loop and append box scores of dates specified
    df = pd.DataFrame()
    for i in range(0, len(date_df)-1):
        date, team, opp = date_df.iloc[i]['DATE'], date_df.iloc[i]['TEAM'], date_df.iloc[i]['OPPONENT']
        bs = get_box_scores(date, team, opp)
        team_bs = bs[team]
    
        team_totals = team_bs.loc[team_bs['PLAYER'] == 'Team Totals']
        
        tm_mp = team_totals['MP'].astype('int').squeeze()
        tm_fga = team_totals['FGA'].astype('int').squeeze()
        tm_fta = team_totals['FTA'].astype('int').squeeze()
        tm_tov = team_totals['TOV'].astype('int').squeeze()
        
        player_totals = team_bs.loc[team_bs['PLAYER'].str.lower() == player_name.lower()]
        
        mp = player_totals['MP'].apply(lambda x: datetime.strptime(x, '%M:%S'))
        mp = mp.apply(lambda x: round(x.minute + (x.second / 60),2))
        mp = mp.squeeze()
        fga = player_totals['FGA'].astype('int').squeeze()
        fta = player_totals['FTA'].astype('int').squeeze()
        tov = player_totals['TOV'].astype('int').squeeze()
        
        totals_df = pd.DataFrame([['player', date,mp,fga,fta,tov],['team', date,tm_mp,tm_fga,tm_fta,tm_tov]], columns=['type', 'DATE', 'MP','FGA','FTA','TOV'])
        
        df = pd.concat([df, totals_df])
        
    return df
    
def filterByLastNGames(date_df, last_n_games=1):
    # find beginning index and date based on last_n_games
    start_idx = max(date_df.index[date_df['DATE'] == date].tolist()[0]-last_n_games, 0)
    start_dt = date_df.iloc[start_idx]['DATE']
    # filter for games between start_dt and date specified above
    date_df = date_df.loc[(date_df['DATE'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(start_dt)) & (date_df['DATE'].apply(lambda x: pd.to_datetime(x)) < date)].reset_index(drop=True)
    
    return date_df

# def getGameUsage(player_name, _date, team, opp_team, return_totals=False):
#     bs = get_box_scores(_date, team, opp_team)
#     team_bs = bs[team]
    
#     team_totals = team_bs.loc[team_bs['PLAYER'] == 'Team Totals']
    
#     tm_mp = team_totals['MP'].astype('int').squeeze()
#     tm_fga = team_totals['FGA'].astype('int').squeeze()
#     tm_fta = team_totals['FTA'].astype('int').squeeze()
#     tm_tov = team_totals['TOV'].astype('int').squeeze()
    
#     player_totals = team_bs.loc[team_bs['PLAYER'].str.lower() == player_name.lower()]
    
#     mp = player_totals['MP'].apply(lambda x: datetime.strptime(x, '%M:%S'))
#     mp = mp.apply(lambda x: round(x.minute + (x.second / 60),2))
#     mp = mp.squeeze()
#     fga = player_totals['FGA'].astype('int').squeeze()
#     fta = player_totals['FTA'].astype('int').squeeze()
#     tov = player_totals['TOV'].astype('int').squeeze()
    
#     usage = 100 * ((fga + 0.44*fta + tov) * (tm_mp/5)) / (mp * (tm_fga + 0.44*tm_fta + tm_tov))
#     ' 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV))'
    
#     df = pd.DataFrame([['player', mp,fga,fta,tov],['team',tm_mp,tm_fga,tm_fta,tm_tov]], columns=['type','MP','FGA','FTA','TOV'])
    
#     if return_totals:
#         return df
#     else:
#         return usage
    
def calcUsage(totals_df):
    
    df = totals_df.groupby('type', as_index=False).sum()
    
    mp = df.loc[df['type'] == 'player']['MP'].squeeze()
    fga = df.loc[df['type'] == 'player']['FGA'].squeeze()
    fta = df.loc[df['type'] == 'player']['FTA'].squeeze()
    tov = df.loc[df['type'] == 'player']['TOV'].squeeze()
    
    tm_mp = df.loc[df['type'] == 'team']['MP'].squeeze()
    tm_fga = df.loc[df['type'] == 'team']['FGA'].squeeze()
    tm_fta = df.loc[df['type'] == 'team']['FTA'].squeeze()
    tm_tov = df.loc[df['type'] == 'team']['TOV'].squeeze()
    
    usage = 100 * ((fga + 0.44*fta + tov) * (tm_mp/5)) / (mp * (tm_fga + 0.44*tm_fta + tm_tov))
    
    return usage

def get_team_game_log(team, year, playoffs=False):
    if playoffs:
        selector = 'div_tgl_basic_playoffs'
    else:
        selector = 'div_tgl_basic'
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2FMIA%2F2022%2Fgamelog%2F&div={selector}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if table:
            df = pd.read_html(str(table))[0]
            df = df.loc[(df['Unnamed: 0_level_0','Rk'].str.isdigit()) | (df['Unnamed: 0_level_0','Rk'].isna())][['Unnamed: 2_level_0','Unnamed: 4_level_0','Team']]
            df.columns = df.columns.droplevel()
            df['TEAM'] = team
            df['MP'] = 240
            df = df.rename(columns={'Date':'DATE', 'Opp':'OPPONENT'})
            
            cols = df.columns.tolist()
            cols = cols[0:1] + cols[-2:-1] + cols[1:2] + cols[-1:] + cols[2:-2]
            df = df[cols]
    return df

def 