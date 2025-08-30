import requests
from bs4 import BeautifulSoup
import re

def get_top5():
    url = "https://www.squashtour.sk/rebricek/dospeli/zeny/#zebricek"

    # Fetch page
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        return []

    top5 = []

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 4:  # Ensure enough columns
            continue

        # Rank
        rank_match = re.match(r'(\d+)', cols[0].get_text(strip=True))
        if not rank_match:
            continue
        rank = int(rank_match.group(1))

        # Name
        name = cols[1].get_text(strip=True)

        # Points (allow decimals)
        points_str = cols[3].get_text(strip=True).replace("\u00a0", "").replace(" ", "")
        try:
            points = float(points_str)
        except ValueError:
            continue

        top5.append({
            "rank": rank,
            "name": name,
            "points": points
        })

        if len(top5) == 5:
            break

    return top5

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
