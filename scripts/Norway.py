import requests
from datetime import datetime, timedelta

def get_latest_monday():
    today = datetime(2025, 8, 16)  # Static date for testing
    days_since_monday = today.weekday()
    last_monday = today - timedelta(days=days_since_monday)
    ranking_date = last_monday.strftime("%Y-%m-%d")
    return ranking_date

def get_top5():
    api_url_base = "https://api.rankedin.com/v1/Ranking/GetRankingsAsync?rankingId=82&rankingType=1&ageGroup=1"
    ranking_date = get_latest_monday()
    api_url = f"{api_url_base}&rankingDate={ranking_date}&weekFromNow=0&language=nl&skip=0&take=10"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://rankedin.com',
        'Referer': 'https://rankedin.com/'
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        players = data.get("Payload", [])[:5]

        top_5 = []
        for p in players:
            top_5.append({
                'rank': str(p.get('Standing', '')),
                'name': p.get('Name', ''),
                'points': str(p.get('ParticipantPoints', {}).get('Points', ''))
            })
        return top_5

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
