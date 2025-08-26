import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://verseny.squash.hu/ranklist/woman"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        table = tables[0]
        if not table:
            return []

        top_5_players = []
        rows = table.find_all('tr')[1:6]  # Skip header, take first 5 rows

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                rank = cols[0].text.strip()
                points = cols[3].text.strip()
                name = cols[1].text.strip()
                top_5_players.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })

        return top_5_players

    except Exception as e:
        print(f"Error scraping Hungary: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
