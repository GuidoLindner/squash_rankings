import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://www.squash.or.at/ranglisten/ranking/"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table')  # Adjust if there are multiple tables
        top_5_players = []

        # Get first 5 data rows (skip header)
        rows = table.find_all('tr')[1:6]

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                rank = cols[0].text.strip()
                points = cols[1].text.strip()
                name = cols[4].text.strip() if cols[4].text.strip() else cols[3].text.strip()
                top_5_players.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })

        return top_5_players

    except Exception as e:
        print(f"Error scraping Austria: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    for player in players:
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
