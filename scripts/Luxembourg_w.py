import requests
from bs4 import BeautifulSoup
import re

def get_top5():
    url = "https://www.fsl.lu/2024_ranking/showrankings.php?admin="

    # The form fields to send (note the spaces around the values—keep them!)
    payload = {
        "admin": "",
        "whatplayers": " AND sexe='f' ",
        "club": "",
        "orderstring": " ORDER by sl_off_ranking DESC ",
        "submitButton": " Send ",
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": url,
    }

    with requests.Session() as s:
        s.headers.update(headers)

        # Get once to establish cookies (some servers care)
        s.get(url)

        # Now post the form selection (women + order by official ranking desc)
        resp = s.post(url, data=payload)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # The rankings live in the table with class="text"
    table = soup.find("table", class_="text")
    if not table:
        return []

    top5 = []
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 3:
            continue

        # first cell must be a pure rank number
        rank_txt = tds[0].get_text(strip=True)
        if not re.fullmatch(r"\d+", rank_txt):
            continue

        # name in 2nd cell; strip tooltip text if present
        name_raw = tds[1].get_text(" ", strip=True)
        name = re.sub(r"click to show improvement-graph.*", "", name_raw, flags=re.I).strip()

        # points is the 3rd cell on this page
        points = tds[2].get_text(strip=True)

        top5.append({"rank": int(rank_txt), "name": name, "points": points})
        if len(top5) == 5:
            break

    return top5

# Test
if __name__ == "__main__":
    players = get_top5()
    if players:
        for p in players:
            print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
    else:
        print("No players found.")
