import requests
from bs4 import BeautifulSoup
import re

def get_top5():
    url = "https://api.leveltech.squashlevels.com/api/classic/players?ranking=-1&club=all&county=all&country=1&show=last6m&matchtype=all&playercat=all&playertype=2&filter_reset=0"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://app.squashlevels.com/players'
    }

    params = {
        'country': '1'  # England's country code
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        content = response.text
        return parse_html_response(content)

    except Exception as e:
        print(f"Error fetching England API data: {e}")
        return []

def parse_html_response(content):
    soup = BeautifulSoup(content, 'html.parser')
    rows = soup.find_all('div', class_='ranking_row_output_div')

    top_5_players = []
    for row in rows:
        rank_elem = row.find('div', class_='ranking_position')
        rank = rank_elem.text.strip() if rank_elem else ''

        name_elem = row.find('div', class_='ranking_name')
        name = name_elem.get_text().strip() if name_elem else ''
        name = re.sub(r'\s+', ' ', name).strip()

        points_elem = row.find('div', class_='ranking_level')
        points = points_elem.text.strip() if points_elem else 'N/A'

        country_elem = row.find('div', class_='ranking_country')
        country = country_elem.text.strip() if country_elem else ''

        if country == 'ENG':
            top_5_players.append({
                'rank': rank,
                'name': name,
                'points': points
            })

        if len(top_5_players) >= 5:
            break

    if len(top_5_players) < 5:
        print(f"Warning: Only found {len(top_5_players)} English players. Check API response at https://app.squashlevels.com/players.")

    return top_5_players

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No English players found. Try checking API parameters at https://app.squashlevels.com/players.")
