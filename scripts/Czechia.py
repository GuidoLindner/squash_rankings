import requests
from bs4 import BeautifulSoup
import re

def get_top5():
    url = "https://czechsquash.cz/zebricek/dospeli/muzi/#zebricek"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            return []

        top5 = []
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            rank_text = cols[0].get_text(strip=True)
            match = re.match(r'(\d+)', rank_text)
            if not match:
                continue
            rank = int(match.group(1))

            name = cols[1].get_text(strip=True)
            points_str = cols[-2].get_text(strip=True).replace("\u00a0", "").replace(" ", "")
            try:
                points = int(points_str)
            except ValueError:
                continue

            top5.append({
                'rank': str(len(top5) + 1),
                'name': name,
                'points': points
            })

            if len(top5) == 5:
                break

        return top5

    except Exception as e:
        print(f"Error scraping Czechia: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
