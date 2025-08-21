from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_vlaanderen_top5():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://squashvlaanderen.toernooi.nl/ranking/category.aspx?id=45911&category=536")

        # --- First popup ("Akkoord") ---
        try:
            akkoord_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'accept') or contains(text(),'Akkoord')]")
                )
            )
            driver.execute_script("arguments[0].click();", akkoord_btn)
            time.sleep(2)
        except:
            pass

        # --- Second popup is inside iframe ---
        try:
            # Wait for the iframe to appear
            iframe = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "iframe[src*='consent']")  # consent iframe
                )
            )
            driver.switch_to.frame(iframe)

            # Now click inside iframe
            accept_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Accept and continue')]")
                )
            )
            driver.execute_script("arguments[0].click();", accept_btn)

            # Switch back to main content
            driver.switch_to.default_content()
            time.sleep(2)
        except:
            pass

        # --- Select latest ranking week ---
        select_element = wait.until(
            EC.presence_of_element_located(
                (By.ID, "ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ddlRankingWeek")
            )
        )
        select = Select(select_element)
        select.select_by_index(0)
        time.sleep(3)

        # --- Scrape top 5 rows ---
        rows = driver.find_elements(By.CSS_SELECTOR, "table.ranking_table tbody tr.ranking_row")
        top5 = []
        for row in rows[:5]:
            cols = row.find_elements(By.TAG_NAME, "td")
            rank = cols[0].text.strip()
            name = cols[2].text.strip()
            points = cols[4].text.strip()
            top5.append({'rank': rank, 'name': name, 'points': points})

        return top5

    finally:
        driver.quit()


# --- Test run ---
if __name__ == "__main__":
    players = get_vlaanderen_top5()
    for p in players:
        print(f"Rank: {p['rank']}, Name: {p['name']}, Points: {p['points']}")
