import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://squash.se/ranking/?_gl=1*1x5fiup*_ga*MjEwMjkxNTcwOS4xNzUzNjMyMjE5*_ga_QVHD4R1NQ5*czE3NTM2MzIyMTkkbzEkZzAkdDE3NTM2MzIyMTkkajYwJGwwJGgw"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        if not table:
            return []

        top5 = []
        rows = table.find_all('tr')[1:6]  # Skip header row, take top 5

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:  # Ensure enough columns exist
                rank = cols[0].text.strip()
                name = cols[1].text.strip()
                points = cols[5].text.strip()
                top5.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })

        return top5

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Sweden rankings: {e}")
        return []

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
