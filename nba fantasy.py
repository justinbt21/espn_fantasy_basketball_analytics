# -*- coding: utf-8 -*-
"""
Created on Tue May 10 19:16:43 2022

@author: Justin Tran
"""

from espn_api.basketball.league import League
import pandas as pd
import bokeh
from datetime import datetime
from dateutil.relativedelta import relativedelta as tDelta
import plotly.express as xp
import plotly.io as pio


# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# import plotly.graph_objs as go

league_id = 64009
year = 2022
espn_s2='AEB4vvlGxZTkNFuii7Cmx1ZaY1FDSiCgnp%2BSYIccw9%2FCWX%2FrmCw%2FY2IlEvNY%2BBjAi3Uox4ZjxmDGSbq1Ejw7%2F5wYtDVDyC1vd4NqZi%2Bg2py9QQp9OS0SkHvEU9wkUicUTv2b%2BdYvyKA3rEfSsGg4saaNnAIZVU93WKrYbqr27bjiIVKRNRdfZWfJtIv0CjgeogmGNilQ0SWXYrxibHBVUq%2BEakONVzJNEYmmhS5Omd73T8ev1Wrp6ZmrFhI%2FsAxHxWMTazJNwcpaSY%2BqHEU9x6KxHivu67b3wKSQ8JbLH84j%2BA%3D%3D'
swid='8048D688-6AF3-4640-83ED-4B55EAC50073'
team_name = 'Lavine La Vida Loca'


desc_stats = ['name'
         , 'position'
         , 'lineupSlot'
         , 'injuryStatus'
]
counting_stats = [ 'MIN'
         , 'FGM'
         , 'FGA'
         , 'FG%'
         , 'FTM'
         , 'FTA'
         , 'FT%'
         , '3PTM'
         , 'REB'
         , 'AST'
         , 'STL'
         , 'BLK'
         , 'PTS'
         , 'TO'
    ]


class teamManager(object):
    
    pio.renderers.default='browser'
    
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 1000)

    def __init__(self, league_id, year, team_name, espn_s2, swid):
        self.league_id = league_id
        self.year = year
        self.team_name = team_name
        self.espn_s2 = espn_s2
        self.swid = swid
        self.league = None
        
        # Initialize functions when teamManager is called
        self._getLeague()
    
    def _getLeague(self):
        self.league = League(league_id=self.league_id, year=self.year, espn_s2=self.espn_s2, swid=self.swid)
        
        return self.league

    # Get Team ID
    def getTeamId(self, teamName: str) -> int:
        league = self.league
        for id in range(0, len(league.teams)):
            if league.teams[id].team_name.lower() == teamName.lower():
               
                return id
        
        raise Exception("That team name does not exist. Check your spelling and try again.") 
        
    def lowerCase(list):
        for i in range(0,len(list)):
            list[i] = list[i].lower()
    
        return list
    
    # Get Team Player Objects
    def getTeamRosterObjs(self, teamName: str):
        league = self.league
        teamId = self.getTeamId(teamName=teamName)
        
        return league.teams[teamId].roster
    
    # Retrieve Stats when passing Player Object(s)
    def getStats(self, playerObjects, year: str=None) -> pd.DataFrame:
        df = pd.DataFrame(columns=desc_stats + counting_stats)
        year_str = f'{year if year else self.year}'
        
        for i in range(0, len(playerObjects)):
            player = pd.DataFrame(index = [0])
            player['name'] = playerObjects[i].name
            player['position'] = playerObjects[i].position
            player['lineupSlot'] = playerObjects[i].lineupSlot
            player['injuryStatus'] = playerObjects[i].injuryStatus
            
            # To add a row of stats, update counting_stats list
            if 'avg' in playerObjects[i].stats[year_str]:
                for j in counting_stats:
                    player[f'{j}'] = round(playerObjects[i].stats[year_str]['avg'][f'{j}'], 1)
            else:
                for j in counting_stats:
                    player[f'{j}'] = 0.0
            
            df = pd.concat([df, player])
    
        
        df.reset_index(inplace=True)
        df.drop(columns='index', inplace=True)
        
        return df
    
    # Leverage getStats to retrieve Stats for owned/FA players
    def getFreeAgentStats(self, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
        league = self.league
        playerObjects = league.free_agents(size=size, position=position)
        
        return self.getStats(playerObjects=playerObjects, year=f'{year if year else self.year}')
    
    def getFreeAgentStats_Last7(self, teamName: str, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
        
        return self.getFreeAgentStats(teamName, f'{year if year else self.year}_last_7')
    
    def getFreeAgentStats_Last15(self, teamName: str, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
        
        return self.getFreeAgentStats(teamName, f'{year if year else self.year}_last_15')
    
    def getFreeAgentStats_Last30(self, teamName: str, size: int=100, position: str=None, year: str=None) -> pd.DataFrame:
        
        return self.getFreeAgentStats(teamName, f'{year if year else self.year}_last_30')
    
    def getRosterStats(self, teamName: str, year: str=None) -> pd.DataFrame:
        playerObjects=self.getTeamRosterObjs(teamName)
        
        return self.getStats(playerObjects=playerObjects, year=f'{year if year else self.year}')
    
    def getRosterStats_Last7(self, teamName: str, year: str=None) -> pd.DataFrame:
        
        return self.getRosterStats(teamName, f'{year if year else self.year}_last_7')
    
    def getRosterStats_Last15(self, teamName: str, year: str=None) -> pd.DataFrame:
        
        return self.getRosterStats(teamName, f'{year if year else self.year}_last_15')
    
    def getRosterStats_Last30(self, teamName: str, year: str=None) -> pd.DataFrame:
        
        return self.getRosterStats(teamName, f'{year if year else self.year}_last_30')
    

    # Get Weekly Games for a team
    def getWeeklyGames(self):
        return None
    
    def tradeEvaluator(self, opp_team_name, players_trading, players_trading_for, graph_data = False):
        team = self.getRosterStats(self.team_name)
        opp_team = self.getRosterStats(opp_team_name)
        
        trading_list = team[team.name.str.lower().isin(lowerCase(players_trading))]
        trading_for_list = opp_team[opp_team.name.str.lower().isin(lowerCase(players_trading_for))]
        
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
        
        trade_eval_stats = new_total_stats - current_total_stats
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
    
    # def tradeEvaluator(current_team, proposed_players=[], received_players=[], season=current_year, last_game_range = None, graph_data = False):
    #   total_players = fantasy_team + received_players

    #   df = getStats(total_players, season, last_game_range = last_game_range)

    #   current_team = df.loc[df['PLAYER_NAME'].str.lower().isin(fantasy_team)]
    #   new_team = df.loc[~df['PLAYER_NAME'].str.lower().isin(proposed_players)]

    #   current_stats = current_team.groupby('PLAYER_NAME').mean() * 3
    #   current_total_stats = current_stats.sum()
    #   current_total_stats['FG_PCT'] = current_total_stats['FGM']/current_total_stats['FGA']
    #   current_total_stats['FG3_PCT'] = current_total_stats['FG3M']/current_total_stats['FG3A']
    #   current_total_stats['FT_PCT'] = current_total_stats['FTM']/current_total_stats['FTA']
    
    #   new_stats = new_team.groupby('PLAYER_NAME').mean() * 3
    #   new_total_stats = new_stats.sum()
    #   new_total_stats['FG_PCT'] = new_total_stats['FGM']/new_total_stats['FGA']
    #   new_total_stats['FT_PCT'] = new_total_stats['FTM']/new_total_stats['FTA']

    #   drop_cols = ['VIDEO_AVAILABLE', 'Player_ID', 'PLUS_MINUS', 'MIN', 'PF', 'FGM', 'FGA', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'OREB', 'DREB']
    #   trade_eval_stats = new_total_stats - current_total_stats
    #   trade_eval_stats = trade_eval_stats.drop(drop_cols)
    #   current_total_stats = current_total_stats.drop(drop_cols)
    
    #   pct_change_stats = trade_eval_stats / current_total_stats
    
    #   df1 = pd.DataFrame(trade_eval_stats, columns = ['Weekly Change'])
    #   df2 = pd.DataFrame(pct_change_stats, columns = ['Percent Change'])
    
    #   chart = df1.merge(df2, 'inner', left_index = True, right_index = True)
    #   graph_bar = [go.Bar(
    #           x = list(pd.DataFrame(pct_change_stats).reset_index()['index']),
    #           y = list(pct_change_stats.round(3))
    #       )]
    #   layout = {
    #               'xaxis': {'title': '% Change'},
    #               'yaxis': {'title': 'Fantasy Category'},
    #               'barmode': 'relative',
    #               'title' : 'Trade Evaluator',
    #               'tickformat': '.0%'
    #           }

    #   bar = plot({'data': graph_bar, 'layout': layout})
    
    #   data = bar if graph_data == True else chart

    #   return data
    
    