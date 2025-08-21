import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://ranking.squash.ch/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        if not table:
            return []

        top5 = []
        rows = table.find_all('tr')[1:6]  # Skip header, take top 5

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 9:  # Ensure enough columns
                rank = cols[0].text.strip()
                firstname = cols[2].text.strip()
                lastname = cols[3].text.strip()
                points = cols[8].text.strip()
                top5.append({
                    'rank': rank,
                    'name': f"{firstname} {lastname}",
                    'points': points
                })

        return top5

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Switzerland rankings: {e}")
        return []

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
