# -*- coding: utf-8 -*-
"""
Created on Fri May 20 21:43:19 2022

@author: Justin Tran
"""

import json
from nba_api.stats.endpoints import CommonAllPlayers, CommonTeamYears, ShotChartDetail, PlayerDashPtShotDefend, LeagueDashPtTeamDefend, PlayerAwards
from nba_api.stats.library.parameters import Season, DefenseCategory
from nba_api.stats.static.players import get_players
from . import constants
import pandas as pd
from time import sleep

_json = CommonAllPlayers(is_only_current_season=1).get_json()


def _api_scrape(_json_str, index=0):
    _json = json.loads(_json_str)
    
    columns = _json['resultSets'][index]['headers']
    values = _json['resultSets'][index]['rowSet']
    
    return pd.DataFrame(values, columns=columns)

class statmanager(object):
    
    def __init__(self):
        # Initialize player and team list so you will not have to repeat requests to get info
        self.player_list = self._getPlayers()
        self.team_list = self._getTeams()
        self.team_def_stats = self.getLeaguePlayerDefStats()

    def _getPlayers(self, is_current=1):
        _json_str = CommonAllPlayers(is_only_current_season=is_current).get_json()
        df = _api_scrape(_json_str)

        return df
    
    def _getTeams(self):
        _json_str = CommonTeamYears().get_json()
        df = _api_scrape(_json_str)
        
        return df
    
    def getPlayerID(self, player_name):
        df = self.player_list
        
        id = df[df['DISPLAY_FIRST_LAST'].str.lower() == player_name.lower()]['PERSON_ID']
        if len(id) == 0:
            static_df = pd.DataFrame(get_players())
            id = static_df[static_df['full_name'].str.lower() == player_name.lower()]['id']
            if len(id) == 0:
                raise Exception('Player could not be found, please try again')
        
        return id.to_string(index=False)
    
    def getTeamID(self, team_name):
        df = self.team_list
        try:
            id = df[df['ABBREVIATION'].str.lower() == team_name.lower()]['TEAM_ID']
            id = id.to_string(index=False)
        except:
            raise Exception('Team Abbreviation could not be found, please try again')
        
        return id
    
    def getLeaguePlayerDefStats(self):
        def_cats=['Overall', '3 Pointers', '2 Pointers', 'Less Than 6Ft', 'Less Than 10Ft', 'Greater Than 15Ft']
        
        dict = {}
        for i in def_cats:
            _json = LeagueDashPtTeamDefend(defense_category=i).get_json()
            def_df = _api_scrape(_json)
            dict[i.lower().replace(' ', '_')] = def_df
            sleep(2) #self throttle requests to prevent getting IP banned
        
        return dict
    
    def getPlayerTeam(self, player_name):
        df = self.player_list
        try:
            id =  df[df['DISPLAY_FIRST_LAST'].str.lower() == player_name.lower()]['TEAM_ID']
            id = id.to_string(index=False)
        except:
            raise Exception('Player could not be found, please try again')
            
        return id
    
    def getPlayerShots(self, player_name, year=Season().default):
        player_id = self.getPlayerID(player_name)
        _json = ShotChartDetail(player_id=player_id, team_id=0, season_nullable=year, context_measure_simple='FGA').get_json()
        df = _api_scrape(_json)
        
        return df
    
    def getPlayerDefStatsDetailed(self, player_name, year=Season().default):
        player_id = self.getPlayerID(player_name)
        _json = PlayerDashPtShotDefend(player_id=player_id, team_id=0, season=year).get_json()
        df = _api_scrape(_json)

        return df

    def getPlayerAwards(self, player_name):
        player_id = self.getPlayerID(player_name)
        _json = PlayerAwards(player_id=player_id).get_json()
        df = _api_scrape(_json)
        
        return df