import requests
from bs4 import BeautifulSoup
import time

def get_top5():
    url = "https://www.sportyhq.com/ranking/group/742?iframe=true&web_view=true&list_only=true&filter=yes&show_title=true&application=widget"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "www.sportyhq.com",
        "Connection": "keep-alive"
    }

    time.sleep(4)  # Avoid rate-limiting

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all('table')
        table = tables[0]

        rows = table.find_all('tr')[1:6]  # Skip header
        top_5_players = []

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                rank = cells[0].text.strip()
                name = cells[2].text.strip()
                points = cells[6].text.strip()
                top_5_players.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })

        return top_5_players

    except Exception as e:
        print(f"Error scraping Portugal: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
