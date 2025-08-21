import requests

def get_top5():
    url = "https://api.ussquash.com/resources/rankings/9/current?divisions=2&pageNumber=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        top_5_players = []
        for player_data in data[:5]:
            rank = player_data.get('ranking', 'N/A')
            name = f"{player_data.get('firstName', '')} {player_data.get('lastName', '')}".strip()
            points = player_data.get('totalPoints', 'N/A')

            top_5_players.append({
                'rank': rank,
                'name': name,
                'points': points
            })

        return top_5_players

    except Exception as e:
        print(f"Error scraping Finland: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
