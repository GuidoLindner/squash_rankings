import requests
from bs4 import BeautifulSoup

URL = "https://www.intooli.at/match22/seasons/24-25/ranks/95/32/2025-07-14/"

def get_top5_women_austria(url=URL):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # find all rows
        rows = soup.select("table tr")  # each row is a <tr>

        top5 = []
        for row in rows[1:6]:  # skip header row, take first 5 players
            cols = row.find_all(["td", "th"])
            if not cols:
                continue
            # from inspecting: col0 = rank, col1 = points, col3 or 4 = name
            rank = cols[0].get_text(strip=True)
            points = cols[1].get_text(strip=True)
            # last column contains the name
            name = cols[-1].get_text(strip=True)

            top5.append({
                "rank": rank,
                "name": name,
                "points": points
            })

        return top5

    except Exception as e:
        print(f"Error scraping Austria (women): {e}")
        return []

if __name__ == "__main__":
    players = get_top5_women_austria()
    for p in players:
        print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
