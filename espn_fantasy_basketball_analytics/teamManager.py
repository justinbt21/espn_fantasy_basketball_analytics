# -*- coding: utf-8 -*-
"""
Created on Tue May 10 19:16:43 2022

@author: Justin Tran
"""
   


from espn_api.basketball.league import League
from .constants import DESC_STATS, COUNTING_STATS
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta as tDelta
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
        self.league = None
        self.teams_dict = None
        self.team_obj = None
        self.position_dict = POSITION_MAP
        self.stat_dict = STATS_MAP
        self.stat_type_dict = STAT_ID_MAP
        self.pro_team_dict = PRO_TEAM_MAP
        self.activity_dict = ACTIVITY_MAP
        
        
        # Initialize league immediately when teamManager is called
        self._getLeague()
        self._get_team_dict()
        self.team_obj = self.getTeamObj(team_id)
    
    def _getLeague(self):
        self.league = League(league_id=self.league_id, year=self.year, espn_s2=self.espn_s2, swid=self.swid)
        
        return self.league
    
    def _get_team_dict(self):
        self.teams_dict = {d.team_id:{'name':d.team_name,
                                      'obj': d} for d in self.league.teams}
        
        return self.teams_dict

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
    def getStats(self, playerObjects, year: str=None) -> pd.DataFrame:
        df = pd.DataFrame(columns=DESC_STATS + COUNTING_STATS)
        year_str = f'{year if year else 0}'
        
        for i in range(0, len(playerObjects)):
            player = pd.DataFrame(index = [0])
            player['name'] = playerObjects[i].name
            player['position'] = playerObjects[i].position
            player['lineupSlot'] = playerObjects[i].lineupSlot
            player['injuryStatus'] = playerObjects[i].injuryStatus
            
            # To add a row of stats, update counting_stats list
            if 'avg' in playerObjects[i].stats[year_str]:
                for j in COUNTING_STATS:
                    player[f'{j}'] = round(playerObjects[i].stats[year_str]['avg'][f'{j}'], 1)
            else:
                for j in COUNTING_STATS:
                    player[f'{j}'] = 0.0
            
            df = pd.concat([df, player])
    
        df.reset_index(inplace=True)
        df.drop(columns='index', inplace=True)
        
        return df
    
    # Leverage getStats to retrieve Stats for owned/FA players
    def getFreeAgentStats(self, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
        league = self.league
        playerObjects = league.free_agents(size=size, position=position)
        df = self.getStats(playerObjects=playerObjects, year=f'{year if year else 0}').drop(columns=['lineupSlot'])

        return df
    
    # def getFreeAgentStats_Last7(self, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
    #
    #     return self.getFreeAgentStats(size, position, f'{year if year else self.year}_last_7')
    #
    # def getFreeAgentStats_Last15(self, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
    #
    #     return self.getFreeAgentStats(size, position, f'{year if year else self.year}_last_15')
    #
    # def getFreeAgentStats_Last30(self, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
    #
    #     return self.getFreeAgentStats(size, position, f'{year if year else self.year}_last_30')
    
    def getRosterStats(self, teamId, year: str=None) -> pd.DataFrame:
        playerObjects=self.getTeamRosterObjs(teamName)
        
        return self.getStats(playerObjects=playerObjects, year=f'{year if year else self.year}')
    
    def getRosterStats_Last7(self, teamName: str, year: str=None) -> pd.DataFrame:
        
        return self.getRosterStats(teamName, f'{year if year else self.year}_last_7')
    
    def getRosterStats_Last15(self, teamName: str, year: str=None) -> pd.DataFrame:
        
        return self.getRosterStats(teamName, f'{year if year else self.year}_last_15')
    
    def getRosterStats_Last30(self, teamName: str, year: str=None) -> pd.DataFrame:
        
        return self.getRosterStats(teamName, f'{year if year else self.year}_last_30')
    def getCurrentMatchup(teamId):
        return None
    
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
    
    def tradeEvaluator(self, opp_team_name, players_trading, players_trading_for, graph_data = False):
        # Get team sats
        team = self.getRosterStats(self.team_name)
        opp_team = self.getRosterStats(opp_team_name)
        
        #Isolate players in trade
        trading_list = team[team.name.str.lower().isin(lowerCase(players_trading))]
        trading_for_list = opp_team[opp_team.name.str.lower().isin(lowerCase(players_trading_for))]
        
        #Replace team with new players
        new_team = team[~team.name.str.lower().isin(lowerCase(players_trading))]
        new_team = pd.concat([new_team, trading_for_list]).reset_index(drop=True)
        
        new_opp_team = opp_team[~opp_team.name.str.lower().isin(lowerCase(players_trading))]
        new_opp_team = pd.concat([opp_team, trading_list]).reset_index(drop=True)
        
        ## Generate current team stats
        drop_cols1 = ['position', 'lineupSlot', 'injuryStatus']
        
        current_stats = team.drop(columns=drop_cols1)
        current_stats = current_stats.groupby('name').mean()
        current_total_stats = current_stats.sum()
        current_total_stats['FG%'] = current_total_stats['FGM']/current_total_stats['FGA']
        current_total_stats['FT%'] = current_total_stats['FTM']/current_total_stats['FTA']
        
        new_stats = new_team.drop(columns=drop_cols1)
        new_stats = new_stats.groupby('name').mean()
        new_total_stats = new_stats.sum()
        new_total_stats['FG%'] = new_total_stats['FGM']/new_total_stats['FGA']
        new_total_stats['FT%'] = new_total_stats['FTM']/new_total_stats['FTA']

        drop_cols2 = ['FGM', 'FGA', 'FTM', 'FTA']
        current_total_stats = current_total_stats.drop(columns=drop_cols2)
        new_total_stats = new_total_stats.drop(columns=drop_cols2)
        
        trade_eval_stats = (new_total_stats - current_total_stats).round(3)
        pct_change_stats = (100.00 * (trade_eval_stats / current_total_stats)).round(2)
        
        df1 = pd.DataFrame(trade_eval_stats, columns = ['Weekly Change'])
        df2 = pd.DataFrame(pct_change_stats, columns = ['Percent Change'])
        
        chart = df1.merge(df2, 'inner', left_index = True, right_index = True)
        graph_bar = xp.bar(pct_change_stats,
                x = list(pd.DataFrame(pct_change_stats).reset_index()['index'])
                , y = list(pct_change_stats.round(3))
                , title = 'Trade Evaluator (in %)'
                , labels = {
                            'x': 'Fantasy Category'        
                            , 'y': '% Change'
                        }
                
            )
       
        data = graph_bar.show() if graph_data == True else chart

        return data


    
