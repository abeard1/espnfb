class Player(object):
    def __init__(self, data):
        self.first_name = data['firstName']
        self.last_name = data['lastName']
        self.draft_rank = data['draftRank']
        self.droppable = data['droppable']
        self.percent_owned = data['percentOwned']
        self.percent_started = data['percentStarted']

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name   
