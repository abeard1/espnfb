import requests
from .player import Player

class Team(object):
    '''Teams are part of the league'''
    def __init__(self, data, league_id, year, cookies):
        self.team_id = data['teamId']
        self.team_abbrev = data['teamAbbrev']
        self.team_name = "%s %s" % (data['teamLocation'], data['teamNickname'])
        self.division_id = data['division']['divisionId']
        self.division_name = data['division']['divisionName']
        self.wins = data['record']['overallWins']
        self.losses = data['record']['overallLosses']
        self.points_for = data['record']['pointsFor']
        self.points_against = data['record']['pointsAgainst']
        self.owner = "%s %s" % (data['owners'][0]['firstName'],
                                data['owners'][0]['lastName'])
        self.schedule = []
        self.scores = []
        self.mov = []
        self.league_id = league_id
        self.cookies = cookies
        self.year = year
        self.ENDPOINT = "http://games.espn.com/fba/api/v2/"
        self._fetch_schedule(data)

    def __repr__(self):
        return 'Team(%s)' % (self.team_name, )

    def _fetch_schedule(self, data):
        '''Fetch schedule and scores for team'''
        matchups = data['scheduleItems']

        for matchup in matchups:
            if not matchup['matchups'][0]['isBye']:
                if matchup['matchups'][0]['awayTeamId'] == self.team_id:
                    score = matchup['matchups'][0]['awayTeamScores'][0]
                    opponentId = matchup['matchups'][0]['homeTeamId']
                else:
                    score = matchup['matchups'][0]['homeTeamScores'][0]
                    opponentId = matchup['matchups'][0]['awayTeamId']
            else:
                score = matchup['matchups'][0]['homeTeamScores'][0]
                opponentId = matchup['matchups'][0]['homeTeamId']

            self.scores.append(score)
            self.schedule.append(opponentId)

    def get_roster(self, week):
        params = {
            'leagueId': self.league_id,
            'seasonId': self.year,
            'teamIds': self.team_id
        }
	
        if week <= 0:
            print('invalid week') # put in real exception here

        params['scoringPeriodId'] = 6 + (week-1)*7

        r = requests.get('%srosterInfo' % (self.ENDPOINT, ), params=params, cookies=self.cookies)
        data = r.json()      

        players = data['leagueRosters']['teams'][0]['slots']
        
        starters = []
        ir = []

        for p in players:
            if 'player' in p:
                if p['slotCategoryId'] == 13:
                    ir.append(Player(p['player']))
                else:
                    starters.append(Player(p['player']))

        return {'starters' : starters, 'ir' : ir }

        '''
        players = data['leagueRosters']['teams'][0]['slots']
        roster = []
        for p in players:
            if 'player' in p:
                player_name = ('%s %s' %(p['player']['firstName'],p['player']['lastName']))
                position = roster_slots[p['slotCategoryId']]
                player_id = p['player']['playerId']
                params = {
                    'leagueId' : self.league_id,
                    'seasonId' : self.year,
                    'teamIds' : self.team_id,
                    'playerId' : player_id,
                    'useCurrentPeriodRealStats' : 'true',
                    'useCurrentPeriodProjectedStats' : 'true'
                }
                if week is not None:
                    params['scoringPeriodId'] = week
                r = requests.get('%splayerInfo' % (self.ENDPOINT, ), params=params, cookies=self.cookies)
                data = r.json()
                if 'appliedStatTotal' in data['playerInfo']['players'][0]['currentPeriodRealStats']:
                    player_score = data['playerInfo']['players'][0]['currentPeriodRealStats']['appliedStatTotal']
                else:
                    player_score = 0
                if 'appliedStatTotal' in data['playerInfo']['players'][0]['currentPeriodProjectedStats']:
                    projected_score = data['playerInfo']['players'][0]['currentPeriodProjectedStats']['appliedStatTotal']
                else:
                    projected_score = 0
                roster.append({'name':player_name,'position':position,'player_id':player_id,'actual score':player_score, 'projected_score':projected_score})
        '''
        #return None

