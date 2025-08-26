import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://realfederaciondesquash.com/rankings/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        tables = soup.find_all("table")
        top5 = []

        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 3:  # Ensure column exists
                    categoria = cols[0].get_text(strip=True)
                    if "ABSFEM" in categoria:  # Women's absolute ranking
                        name = cols[3].get_text(strip=True)
                        points = cols[6].get_text(strip=True) if len(cols) > 2 else "N/A"
                        top5.append({
                            "rank": str(len(top5) + 1),
                            "name": name,
                            "points": points
                        })
                        if len(top5) == 5:
                            break
            if len(top5) == 5:
                break

        return top5

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Spain rankings: {e}")
        return []

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
