import requests
from bs4 import BeautifulSoup
import time

def get_top5():
    url = "https://www.squashireland.ie/tournaments-competitions/rankings/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.squashireland.ie/",
        "Connection": "keep-alive"
    }

    time.sleep(1)  # Avoid rate-limiting

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        woman_header = soup.find('h3', string=lambda text: text and ('Women' in text or 'Senior Ranking - Women' in text))
        if not woman_header:
            return []

        table = woman_header.find_next('table')
        if not table:
            return []

        rows = table.find_all('tr')[1:]  # Skip header
        top_5_players = []

        for row in rows[:5]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                rank = cells[0].text.strip()
                name = cells[1].text.strip()
                points = cells[2].text.strip()
                top_5_players.append({
                    'rank': rank,
                    'name': name,
                    'points': points
                })

        return top_5_players

    except Exception as e:
        print(f"Error scraping Ireland: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
