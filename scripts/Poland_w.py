import requests
from bs4 import BeautifulSoup
import re

def get_top5():
    url = "https://bo5.pl/ranking/ajax/getRankingPlayers.php?ranking_record_id=17158&_=1756197614919"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        top_5 = []
        for player_data in data.get('aaData', [])[:5]:
            rank = player_data.get('position', '').strip()
            points = player_data.get('points', '').strip()
            player_html = player_data.get('player', '')
            name = BeautifulSoup(player_html, 'html.parser').get_text()
            name = re.sub(r'\s+', ' ', name).strip()

            top_5.append({
                'rank': rank,
                'name': name,
                'points': points
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
