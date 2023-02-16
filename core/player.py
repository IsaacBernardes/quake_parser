
class Player:

    def __init__(self, player_id, username, character):
        self.match_id = player_id
        self.username = username
        self.character = character
        self.kills = []
        self.deaths = []
        self.world_deaths = 0
        self.suicides = 0

    def add_kill(self, user_killed, timestamp):
        self.kills.append(dict(
            victim=user_killed.username,
            timestamp=timestamp
        ))

    def add_death(self, killed_by, timestamp):
        if killed_by is None:
            self.world_deaths += 1
            self.deaths.append(dict(
                killer="<world>",
                timestamp=timestamp
            ))
        else:
            self.deaths.append(dict(
                killer=killed_by.username,
                timestamp=timestamp
            ))

    def add_suicide(self, timestamp):
        self.suicides += 1
        self.deaths.append(dict(
            killer=self.match_id,
            timestamp=timestamp
        ))

    def score(self) -> dict:
        return dict(
            kills=max(len(self.kills) - self.world_deaths, 0),
            deaths=len(self.deaths),
            world_deaths=self.world_deaths,
            suicides=self.suicides,
        )

    def disconnect(self):
        self.match_id = None

    def __repr__(self):
        return str(dict(
            match_id=self.match_id,
            username=self.username,
            character=self.character,
            kills=len(self.kills),
            deaths=len(self.deaths),
            suicides=self.suicides
        ))

    def __str__(self):
        return str(dict(
            username=self.username,
            character=self.character,
            kills=len(self.kills),
            deaths=len(self.deaths),
            suicides=self.suicides
        ))
