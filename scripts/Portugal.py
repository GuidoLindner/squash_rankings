from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

# Suppress ChromeDriver logging (DevTools messages)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)

# Set up Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress DevTools messages
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Navigate to the rankings page
    url = "https://fnsquash.pt/home-2/competicao/ranking-nacional-masculino/"
    driver.get(url)

    # Wait for the rankings table or container to load (timeout after 10 seconds)
    # Try to find a table or div container (adjust selector as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table")) or
        EC.presence_of_element_located((By.CLASS_NAME, "ranking-table"))
    )

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Try to find a table first
    table = soup.find("table")
    if table:
        # Extract rows from the table (skip header)
        rows = table.find_all("tr")[1:6]  # Get top 5 rows
        if not rows:
            print("Error: No player rows found in table")
            with open("response.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to response.html for debugging")
            exit(1)

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:  # Ensure enough columns
                rank = cols[0].text.strip()
                name = cols[1].text.strip()
                points = cols[5].text.strip() if len(cols) > 5 else "N/A"
                print(f"Rank: {rank}, Name: {name}, Points: {points}")
            else:
                print(f"Warning: Insufficient columns in row: {row}")
    else:
        # Try to find a div-based structure (similar to France)
        results = soup.find("div", class_="ranking-table") or soup.find("div", class_="wrapper results")
        if not results:
            print("Error: Could not find rankings table or div container")
            with open("response.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to response.html for debugging")
            exit(1)

        # Extract rows (assuming div-based structure like France)
        rows = results.find_all("div", class_="row")[1:6]
        if not rows:
            print("Error: No player rows found in div structure")
            with open("response.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to response.html for debugging")
            exit(1)

        for row in rows:
            rank = row.find("div", class_="rank center") or row.find("div", class_="rank")
            name = row.find("div", class_="name bold") or row.find("div", class_="name")
            points = row.find("div", class_="points center") or row.find("div", class_="points") or row.find("div", class_="moyenne center")
            if not all([rank, name, points]):
                print(f"Warning: Missing data in row: {row}")
                continue
            print(f"Rank: {rank.text.strip()}, Name: {name.text.strip()}, Points: {points.text.strip()}")

except Exception as e:
    print(f"Error: {e}")
    with open("response.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Page source saved to response.html for debugging")
finally:
    driver.quit()