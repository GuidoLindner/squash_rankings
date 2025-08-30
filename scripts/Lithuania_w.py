import requests
from datetime import datetime, timedelta

def get_latest_monday():
    today = datetime(2025, 8, 16)  # Static date for testing
    days_since_monday = today.weekday()
    last_monday = today - timedelta(days=days_since_monday)
    ranking_date = last_monday.strftime("%Y-%m-%d")
    week = last_monday.isocalendar()[1]
    year = last_monday.isocalendar()[0]
    return ranking_date, week, year

def get_top5():
    api_url_base = "https://api.rankedin.com/v1/Ranking/GetRankingsAsync?rankingId=6025&rankingType=2&ageGroup=13"
    try:
        ranking_date, week, year = get_latest_monday()
        api_url = f"{api_url_base}&rankingDate={ranking_date}&weekFromNow=0&language=en&skip=0&take=10&_=1756192942112"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Origin': 'https://rankedin.com',
            'Referer': 'https://rankedin.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }

        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        players = data.get("Payload", [])
        if not players or not isinstance(players, list):
            return []

        top_5 = []
        for player in players[:5]:
            rank = str(player.get('Standing', ''))
            name = player.get('Name', '')
            points = str(player.get('ParticipantPoints', {}).get('Points', ''))
            top_5.append({'rank': rank, 'name': name, 'points': points})

        return top_5

    except Exception as e:
        print(f"Error scraping Lithuania: {e}")
        return []

# Print block for testing
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
