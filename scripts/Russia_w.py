import requests

def get_top5():
    api_url = "https://rating-api.russiansquash.ru/api/rating?gender=FEMALE"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Authorization': 'SphoPMbbwlhyiDwb4P4kAJYRSblU9vnl2sd6l4j6nFOxpG5MZnBnWOf2pcUskUsa',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Origin': 'https://russiansquash.ru',
            'Referer': 'https://russiansquash.ru/',
        }

        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        players = data.get("rating", [])
        if not players or not isinstance(players, list):
            return []

        top_5_players = []
        for i, player in enumerate(players[:5], 1):
            rank = str(player.get('place', i))
            name = player.get('user', {}).get('name', '')
            points = str(player.get('rating', ''))
            top_5_players.append({
                'rank': rank,
                'name': name,
                'points': points
            })

        return top_5_players

    except Exception:
        return []

# Print block for standalone testing
if __name__ == "__main__":
    players = get_top5()
    if players:
        for p in players:
            print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
    else:
        print("No players found.")
