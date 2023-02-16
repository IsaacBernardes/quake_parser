from typing import List
from core.player import Player


class Match:

    def __init__(self, name):
        self.name = name
        self.total_kills = 0
        self.time_elapsed = None
        self.players: List[Player] = []

    def finish_match(self, finished_at):
        self.time_elapsed = finished_at

