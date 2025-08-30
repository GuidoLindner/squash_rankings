import requests
from bs4 import BeautifulSoup

def get_top5():
    url = "https://www.squash-liga.com/bundesliga/rangliste/herren.html"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', id='table_sorter')  # Find the specific table by id
        if not table:
            return []

        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]
        if not rows:
            return []

        top_5_players = []
        for row in rows[:5]:
            cells = row.find_all('td')
            if len(cells) >= 9:
                pos = cells[0].text.strip()
                last_name = cells[1].text.strip()
                first_name = cells[2].text.strip()
                total_points = cells[8].text.strip()

                top_5_players.append({
                    'rank': pos,
                    'name': f"{first_name} {last_name}",
                    'points': total_points
                })

        return top_5_players

    except Exception as e:
        print(f"Error scraping Germany: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
