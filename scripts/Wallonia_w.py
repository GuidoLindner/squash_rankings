import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://www.sportyhq.com/ranking/group/2004?matrix=&iframe=true&list_only=true&filter=yes&criteria=undefined&view=&filter_club_id=&show_all=&show_title=true&sportyhq_csrf_token=92d14cc8051b75eeeaa2883eb6fe8929"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table.ranking_table tbody tr.ranking_row")

        top5 = []
        for row in rows[:5]:
            cols = row.find_all("td")
            rank = cols[0].get_text(strip=True)
            name = cols[2].get_text(strip=True)
            points = cols[4].get_text(strip=True)
            top5.append({
                'rank': rank,
                'name': name,
                'points': points
            })

        return top5

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wallonia rankings: {e}")
        return []

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
