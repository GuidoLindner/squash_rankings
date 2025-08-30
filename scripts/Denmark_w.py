import requests

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "language": "da"
}

def get_top5():
    url = "https://www.squashportalen.dk/api/reports/rankings/lists"

    payload = {
        "pageLimit": 50,
        "currentPage": 1,
        "homeClubId": None,
        "awayClubId": None,
        "playerName": None,
        "runId": "189",  # update manually if needed
        "sex": "D",
        "calculatedAsOf": None
    }

    try:
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        rankings = data.get("result", {}).get("rankings", [])
        if not rankings:
            return []

        top5_players = []
        for player in rankings[:5]:
            rank = player.get("rank", "N/A")
            name = player.get("playerName", "Unknown")
            points_raw = str(player.get("pointsF", "N/A"))
            points = points_raw.replace(".", "").replace(",", ".")  # convert e.g., 6.495,00 → 6495.00
            top5_players.append({
                'rank': rank,
                'name': name,
                'points': points
            })

        return top5_players

    except Exception as e:
        print(f"Error scraping Denmark: {e}")
        return []

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
