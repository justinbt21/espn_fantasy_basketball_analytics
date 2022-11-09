# -*- coding: utf-8 -*-
"""
Created on Tue May 10 19:16:43 2022

@author: Justin Tran
"""

from espn_api.basketball.league import League
from espn_fantasy_basketball_analytics.constants import DESC_STATS, COUNTING_STATS, ROSTER_COLS, FA_COLS
import pandas as pd
import plotly.express as xp
from espn_api.basketball.constant import STAT_ID_MAP, POSITION_MAP, ACTIVITY_MAP, PRO_TEAM_MAP, STATS_MAP

# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# import plotly.graph_objs as go

class teamManager(object):
    
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 1000)

    def __init__(self, league_id, team_id, year, espn_s2, swid):
        self.league_id = league_id
        self.year = year
        self.espn_s2 = espn_s2
        self.swid = swid
        self.league = League(league_id=self.league_id, year=self.year, espn_s2=self.espn_s2, swid=self.swid)
        self.teams_dict = {d.team_id:{'name':d.team_name, 'obj': d} for d in self.league.teams}
        self.team_obj = self.league.get_team_data(3)
        self.currMatchPeriod = self.league.currentMatchupPeriod
        self.currMatchupObj = self.team_obj.schedule[self.currMatchPeriod-1]
        self.position_dict = POSITION_MAP
        self.stat_dict = STATS_MAP
        self.stat_type_dict = STAT_ID_MAP
        self.pro_team_dict = PRO_TEAM_MAP
        self.activity_dict = ACTIVITY_MAP

    # Get Team ID
    def getTeamId(self, teamName: str) -> int:
        for k, v in self.teams_dict.items():
            if v.lower() == teamName.lower():
               
                return k
        
        raise Exception("That team name does not exist. Check your spelling and try again.")

    def getTeamName(self, teamId: int) -> str:
        name = self.teams_dict[teamId]['name']

        return name

    def getTeamObj(self, teamId):
        obj = self.teams_dict[teamId]['obj']

        return obj
        
    def lowerCase(list):
        for i in range(0,len(list)):
            list[i] = list[i].lower()
    
        return list
    
    # Get Team Player Objects
    def getTeamRosterObjs(self, teamId):
        objs = self.teams_dict[teamId]['obj'].roster
        
        return objs
    
    # Retrieve Stats when passing Player Object(s)
    def getStats(self, playerObjects, year: int=None, last_d: int=None) -> pd.DataFrame:

        lookback = '_total' if last_d is None else f'_last_{last_d}'
        year_str = f'{year if year else self.year}{lookback}'
        df = pd.DataFrame(columns=DESC_STATS + COUNTING_STATS)
        
        for i in range(0, len(playerObjects)):
            player = pd.DataFrame(index = [0])
            player['name'] = playerObjects[i].name
            player['position'] = playerObjects[i].position
            player['lineupSlot'] = playerObjects[i].lineupSlot
            player['injuryStatus'] = playerObjects[i].injuryStatus
            
            # To add a row of stats, update counting_stats list
            if 'avg' in playerObjects[i].stats[year_str]:
                for j in COUNTING_STATS:
                    if j not in ['FG%','FT%']:
                        player[f'{j}'] = round(playerObjects[i].stats[year_str]['avg'][f'{j}'], 1)
                    else:
                        player[f'{j}'] = round(playerObjects[i].stats[year_str]['avg'][f'{j}'], 3)
            else:
                for j in COUNTING_STATS:
                    player[f'{j}'] = 0.0
            
            df = pd.concat([df, player])
    
        df.reset_index(inplace=True)
        df.drop(columns='index', inplace=True)
        
        return df
    
    # Leverage getStats to retrieve Stats for owned/FA players
    def getFreeAgentStats(self, size: int=100, position: str=None, year: int=None, last_d: int=None) -> pd.DataFrame:
        league = self.league
        playerObjects = league.free_agents(size=size, position=position)
        # need to change later cause it resultset for current season stats is not available in API
        df = self.getStats(playerObjects=playerObjects, year=year if year else self.year, last_d=last_d).drop(columns=['lineupSlot'])
        df.columns = FA_COLS

        return df
    
    def getRosterStats(self, teamId, year: int=None, last_d: int=None) -> pd.DataFrame:
        playerObjects=self.getTeamRosterObjs(teamId)
        # need to change later cause it resultset for current season stats is not available in API
        df = self.getStats(playerObjects=playerObjects, year=year if year else self.year, last_d=last_d)
        df.columns = ROSTER_COLS
        
        return df

    # def prep_prediction_stats(playerName, gameDate):
    #     player_df = get_game_logs(playerName, self.year)
    #     team_df = get_team_ratings(season_end_year=self.year)
    #     cols = ['MP', 'FG', 'FGA', '3P', 'TRB', 'AST', 'STL', 'BLK', 'PTS', 'PF']
        
    #     stats = player_df.copy()
    #     stats = stats[cols]      
        
    #     stats_dict = {}
    #     stats['MP'] = stats['MP'].apply(lambda x: datetime.strptime(x, '%M:%S'))
    #     stats['MP'] = stats['MP'].apply(lambda x: round(x.minute + (x.second / 60),2))
    #     for c in stats.columns:
            
    #         stats_dict[c] = (round(stats[c].astype(int).mean(), 2), round(stats[c].astype(int).std()), 2)
        
    
    # def predict_player_stats(playerName: str, oppTeam: str, gameDate: str):
        
    

    # Get Weekly Games for a team
    def getWeeklyGames(self):
        return None



    
