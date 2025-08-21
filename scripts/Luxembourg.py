import requests
from bs4 import BeautifulSoup
import re

def get_top5():
    url = "https://www.fsl.lu/2024_ranking/showrankings.php"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            raise RuntimeError("Rankings table not found")

        top_5_players = []
        rows = table.find_all('tr')[5:10]  # Top 5 players rows

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                rank = cols[0].text.strip()
                name = re.sub(r'click to show improvement-graph.*', '', cols[1].text.strip()).strip()
                points = cols[2].text.strip()
                top_5_players.append({'rank': rank, 'name': name, 'points': points})

        return top_5_players

    except Exception as e:
        print(f"Error scraping Luxembourg: {e}")
        return []

# Print block for testing
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
