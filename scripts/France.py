from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

def get_top5():
    # Suppress ChromeDriver logging (DevTools messages)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('webdriver_manager').setLevel(logging.WARNING)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress DevTools messages

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://www.squashnet.fr/classements"
        driver.get(url)

        # Wait for the results wrapper to load (timeout 10s)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wrapper.results"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find("div", class_="wrapper results")
        if not results:
            return []

        top5_players = []
        rows = results.find_all("div", class_="row")[1:6]  # Skip header, take top 5

        for row in rows:
            rank_elem = row.find("div", class_="rank center")
            name_elem = row.find("div", class_="name bold")
            moyenne_elem = row.find("div", class_="moyenne center")

            if not all([rank_elem, name_elem, moyenne_elem]):
                continue

            top5_players.append({
                'rank': rank_elem.text.strip(),
                'name': name_elem.text.strip(),
                'points': moyenne_elem.text.strip()
            })

        return top5_players

    except Exception as e:
        print(f"Error scraping France: {e}")
        return []

    finally:
        driver.quit()

# Print block for testing when running the script directly
if __name__ == "__main__":
    players = get_top5()
    if players:
        for player in players:
            print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
    else:
        print("No players found.")
