import requests
from datetime import datetime, timedelta

def get_latest_monday():
    # Static date for testing; replace with datetime.now() for production
    today = datetime(2025, 8, 16)
    days_since_monday = today.weekday()
    last_monday = today - timedelta(days=days_since_monday)
    ranking_date = last_monday.strftime("%Y-%m-%d")
    week = last_monday.isocalendar()[1]
    year = last_monday.isocalendar()[0]
    return ranking_date, week, year

def get_top5():
    api_url_base = "https://api.rankedin.com/v1/Ranking/GetRankingsAsync?rankingId=6006&rankingType=1&ageGroup=1"
    try:
        ranking_date, week, year = get_latest_monday()
        api_url = f"{api_url_base}&rankingDate={ranking_date}&weekFromNow=6&language=en&skip=0&take=10&_=1755429271055"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Origin': 'https://rankedin.com',
            'Referer': 'https://rankedin.com/',
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        players = data.get("Payload", [])
        if not players or not isinstance(players, list):
            return []

        top_5_players = []
        for player in players[:5]:
            rank = str(player.get('Standing', ''))
            name = player.get('Name', '')
            points = str(player.get('ParticipantPoints', {}).get('Points', ''))
            top_5_players.append({
                'rank': rank,
                'name': name,
                'points': points
            })

        return top_5_players

    except Exception:
        return []

# Print block for standalone testing
if __name__ == "__main__":
    players = get_top5()
    if players:
        for p in players:
            print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
    else:
        print("No players found.")
