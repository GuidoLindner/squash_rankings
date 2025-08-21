import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://www.federsquash.it/attivita-federale/classifiche-federali/ranking-maschile/ranking.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            return []

        rows = table.find_all('tr')[1:]  # Skip header
        top_5_players = []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 6:
                rank = cols[0].text.strip()
                name = cols[1].text.strip()
                points = cols[5].text.strip()
                top_5_players.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })
                if len(top_5_players) == 5:
                    break

        return top_5_players

    except requests.exceptions.RequestException as e:
        print(f"Error scraping Italy: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
