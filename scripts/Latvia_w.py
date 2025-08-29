import re
import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://www.squash.lv/rankings?utf8=%E2%9C%93&rank_type=F&player_name="

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table")
        if not table:
            return []

        tbody = table.find("tbody") or table
        top_5 = []

        for tr in tbody.find_all("tr", recursive=False):
            tds = tr.find_all("td", recursive=False)
            if len(tds) < 3:
                continue

            rank_text = tds[0].get_text(strip=True)
            match = re.match(r'^\d+', rank_text)  # only take the first number
            if not match:
                continue
            rank = int(match.group(0))

            match = re.match(r'(\d+)', rank_text)
            if not match:
                continue
            rank = int(match.group(1))

            # Name: prefer the first link
            name_cell = tds[1]
            a = name_cell.find("a")
            if a:
                name = a.get_text(" ", strip=True)
            else:
                raw = name_cell.get_text(" ", strip=True)
                parts, seen = raw.split(), set()
                name = " ".join([p for p in parts if not (p in seen or seen.add(p))])

            points = tds[2].get_text(strip=True).replace("\xa0", "")

            top_5.append({
                "rank": rank,
                "name": name,
                "points": points
            })

            if len(top_5) == 5:
                break

        return top_5

    except Exception as e:
        print(f"Error scraping Latvia: {e}")
        return []

# Print block for testing
if __name__ == "__main__":
    players = get_top5()
    if players:
        for p in players:
            print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
    else:
        print("No players found.")
