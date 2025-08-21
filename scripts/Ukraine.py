import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://squash.ua/en/rejting"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            return []

        top5 = []
        rows = table.find_all('tr')[1:6]  # skip header, take top 5
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                rank = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                points = cols[4].get_text(strip=True)
                top5.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })

        return top5

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Ukraine rankings: {e}")
        return []

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
