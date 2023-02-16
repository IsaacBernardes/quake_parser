import re
import math
from datetime import time
from typing import List, Optional
from core.match import Match
from core.player import Player


class Parser:

    def __init__(self, file_path):
        file = open(file_path, 'r')
        unformatted_log = file.read()
        file.close()

        lines = unformatted_log.split("\n")
        self.finished_matches: List[Match] = []
        self.under_analysis_match: Optional[Match] = None

        last_timestamp = time(0, 0, 0)
        for line in lines:
            last_timestamp = self._process_line(line, last_timestamp)

    def _process_line(self, line, last_timestamp) -> time:
        line = str(line).strip()
        words = line.split(maxsplit=2)

        if len(words) < 3:

            if len(words) > 0:
                timestamp = self._convert_to_time(words[0])
                if timestamp < last_timestamp:
                    self._finish_action(last_timestamp.strftime("%H:%M:%S"))
                return timestamp
            else:
                return last_timestamp

        if len(words[0]) < 4:
            words = line.split(maxsplit=3)
            words = words[1:3]

            if len(words) < 3:
                if len(words) > 0:
                    timestamp = self._convert_to_time(words[0])
                    if timestamp < last_timestamp:
                        self._finish_action(last_timestamp.strftime("%H:%M:%S"))
                    return timestamp
                else:
                    return last_timestamp

        timestamp = self._convert_to_time(words[0])

        command = words[1][:-1]
        comment = words[2]

        if command == "InitGame":
            self._start_action("match_" + str(len(self.finished_matches) + 1))
        elif command == "ClientUserinfoChanged":
            self._player_action(comment)
        elif command == "Kill":
            self._kill_action(comment, timestamp.strftime("%H:%M:%S"))
        elif command == "ClientDisconnect":
            self._disconnect_player_action(comment)
        elif command == "Exit":
            self._finish_action(timestamp.strftime("%H:%M:%S"))

        return timestamp

    def _start_action(self, name):
        match = Match(name)
        self.under_analysis_match = match

    def _player_action(self, log: str):
        if self.under_analysis_match is not None:
            match_user_id, user_info = log.split(maxsplit=1)
            user_info = user_info.split('\\')

            match_user_id = int(match_user_id)
            username = self._remove_special_characters(user_info[1])
            character = user_info[5].split('/')[0]

            try:
                user = next(player for player in self.under_analysis_match.players if player.username == username)
            except:
                user = None

            if user is None:
                user = Player(match_user_id, username, character)
                self.under_analysis_match.players.append(user)
            else:
                user.match_id = match_user_id
                user.username = username
                user.character = character

    def _disconnect_player_action(self, log):
        match_id = int(log)

        try:
            user = next(player for player in self.under_analysis_match.players if player.match_id == match_id)
            if user is not None:
                user.disconnect()
        except:
            pass

    def _kill_action(self, log: str, timestamp: str):
        if self.under_analysis_match is not None:
            killer_id, victim_id, weapon_id, _ = log.split(maxsplit=3)
            killer_id = int(killer_id)
            victim_id = int(victim_id)

            try:
                killer = next(player for player in self.under_analysis_match.players if player.match_id == killer_id)
            except:
                killer = None

            try:
                victim = next(player for player in self.under_analysis_match.players if player.match_id == victim_id)
            except:
                victim = None

            if killer is not None and victim is not None:
                self.under_analysis_match.total_kills += 1
                if killer.match_id == victim.match_id:
                    killer.add_suicide(timestamp)
                else:
                    killer.add_kill(victim, timestamp)
                    victim.add_death(killer, timestamp)

            elif victim is not None:
                self.under_analysis_match.total_kills += 1
                victim.add_death(killer, timestamp)

    def _finish_action(self, finished_at):
        if self.under_analysis_match is not None:
            self.under_analysis_match.finish_match(finished_at=finished_at)
            self.finished_matches.append(self.under_analysis_match)
            self.under_analysis_match = None

    def _convert_to_time(self, time_str: str) -> time:

        hours = 0
        minutes = 0
        seconds = 0

        if time_str is not None:
            _hours = 0
            _minutes, _seconds = time_str.split(":")
            _minutes = int(_minutes)
            _seconds = int(_seconds)

            if _seconds > 59:
                _minutes += math.floor(_seconds / 60)
                _seconds = _seconds % 60

            if _minutes > 59:
                _hours += math.floor(_minutes / 60)
                _minutes = _minutes % 60

            hours = _hours
            minutes = _minutes
            seconds = _seconds

        return time(hours, minutes, seconds)

    def _remove_special_characters(self, input_string):
        return re.sub(r'[^\w\s]', '', input_string)
