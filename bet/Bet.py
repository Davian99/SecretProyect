class Bet():
    def __init__(self, teams, bets):
        self.teams = [x.strip().upper() for x in teams]
        self.real_teams = []
        self.bets = [float(x.replace(',', '.')) for x in bets]
        self.date_time = None
        self.link = None
        self.house = None
        self.sport = None
    
    def is_error(self):
        if len(self.real_teams) < 2 or len(self.bets) < 2:
            return True
        return False

    def __repr__(self):
        if self.is_error():
            return f"ERROR BET ({self.teams})"
        return f"{self.real_teams[0]} ({self.bets[0]}) x {self.real_teams[1]} ({self.bets[1]})"
    
    def __eq__(self, x):
        if self.is_error() or x.is_error():
            return False
        return self.real_teams == x.real_teams
    
    def hash(self):
        if self.is_error():
            return None
        return f"{self.real_teams[0]}{self.real_teams[1]}".replace(' ', '')