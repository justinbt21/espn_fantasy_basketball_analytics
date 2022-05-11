# -*- coding: utf-8 -*-
"""
Created on Tue May 10 19:16:43 2022

@author: Justin Tran
"""

import basketball_reference_scraper
from espn_api.basketball.league import League
import pandas
import bokeh

league_id = 64009
year = 2022
espn_s2='AEB4vvlGxZTkNFuii7Cmx1ZaY1FDSiCgnp%2BSYIccw9%2FCWX%2FrmCw%2FY2IlEvNY%2BBjAi3Uox4ZjxmDGSbq1Ejw7%2F5wYtDVDyC1vd4NqZi%2Bg2py9QQp9OS0SkHvEU9wkUicUTv2b%2BdYvyKA3rEfSsGg4saaNnAIZVU93WKrYbqr27bjiIVKRNRdfZWfJtIv0CjgeogmGNilQ0SWXYrxibHBVUq%2BEakONVzJNEYmmhS5Omd73T8ev1Wrp6ZmrFhI%2FsAxHxWMTazJNwcpaSY%2BqHEU9x6KxHivu67b3wKSQ8JbLH84j%2BA%3D%3D'
swid='8048D688-6AF3-4640-83ED-4B55EAC50073'
team_name = 'Lavine La Vida Loca'


class teamManager(object):

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
    def _getTeamId(self, alt_team_name=None) -> int:
        league = self.league
        team = alt_team_name if alt_team_name else self.team_name
        for id in range(0, len(league.teams)):
            if league.teams[id].team_name.lower() == team.lower():
                if alt_team_name:
                    self.opp_teamId = id
                    return self.opp_teamId
                else:
                    self.teamId = id
                    
    
    # Get Team Player Objects
    def _getTeamRosterObjs(self):
        league = self.league
        return league.teams[self.teamId].roster

    # Get Weekly Games for a team
    def _getWeeklyGames(self):
        return None
    
    def _getRosterStats(self):
        return None
    
    def tradeEvaluator(self, opp_team_name, player_list):
        return None
    
    