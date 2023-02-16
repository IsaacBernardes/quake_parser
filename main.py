import json

from core.parser import Parser


def main():
    log_parser = Parser('games.log')

    json_matches = []
    for match in log_parser.finished_matches:
        json_matches.append({
            match.name: dict(
                total_kills=match.total_kills,
                duration=match.time_elapsed,
                players=[{player.username: player.score()} for player in match.players]
            )
        })

    print(json.dumps(json_matches, indent=4))


if __name__ == "__main__":
    main()
