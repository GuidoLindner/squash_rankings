import requests
from bs4 import BeautifulSoup

def get_top5():
    url = 'https://www.squashnet.fr/index.php'
    referrer = 'https://www.squashnet.fr/classements'

    payload = {
        'ic_a': '56ed9559ce254f5d94fdcf45090b370f',
        'ic_ajax': '1',
        'month': '35',
        'name': '',
        'ligue': '-1',
        'catage': '-1',
        'clt': '-1',
        'genre': '6',
        'assimilate': '161',
        'integrate': '161',
        'ic_t': 'search_results',
        'ic_mform': '1',
        'id': 'ligue',
        'ic_ajax': '1'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.squashnet.fr',
        'Priority': 'u=1, i',
        'Referer': referrer,
        'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
    }

    session = requests.Session()
    session.headers.update(headers)

    # First, GET the referrer page to set any necessary cookies
    session.get(referrer)

    # Then, POST the request
    response = session.post(url, data=payload, timeout=15)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the results wrapper
    results_div = soup.find('div', class_='wrapper results')
    if not results_div:
        print("No results found.")
        return []

    # Find all rows, skip the header (first row)
    rows = results_div.find_all('div', class_='row')[1:6]  # Top 5

    top_5 = []
    for row in rows:
        cells = row.find_all('div')
        if len(cells) >= 9:
            player = {
                'points': cells[0].text.strip().replace('male', ''),  # Remove 'male' prefix
                'name': cells[1].text.strip(),
                'rank': cells[3].text.strip(),
            }
            top_5.append(player)

    return top_5

if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")