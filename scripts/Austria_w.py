import requests
from bs4 import BeautifulSoup

URL = "https://www.intooli.at/match22/seasons/24-25/ranks/95/32/2025-07-14/"

def get_top5(url=URL):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        tables = soup.find_all('table')
        table = tables[1]

        # all rows after header
        rows = table.find_all('tr')[1:]  

        top5 = []
        for row in rows:
            cols = [c.text.strip() for c in row.find_all('td')]
            if len(cols) >= 4:  # adjust based on table layout
                rank = cols[0]
                name = cols[4]  
                points = cols[1]  # points likely here
                if rank.isdigit():  # skip blank rows
                    top5.append({
                        'rank': rank,
                        'name': name.strip("| ").strip(),
                        'points': points
                    })
            if len(top5) == 5:
                break

        return top5

    except Exception as e:
        print(f"Error scraping Austria (women): {e}")
        return []

if __name__ == "__main__":
    players = get_top5()
    for p in players:
        print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
