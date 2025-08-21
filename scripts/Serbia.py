import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_top5():
    url = "http://skvos.rs/rngl/rngl-muskarci/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)),
        before_sleep=lambda retry_state: logging.info(f"Retrying... Attempt {retry_state.attempt_number}")
    )
    def fetch_page():
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    
    try:
        response = fetch_page()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table')
        if not table:
            logging.warning("No table found on the page. Check the URL or table structure.")
            return []
        
        top5 = []
        rows = table.find_all('tr')[1:6]  # Skip header, take first 5 rows
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                rank = cols[0].text.strip() or "N/A"
                name = cols[1].text.strip() or "N/A"
                points = cols[2].text.strip() if len(cols) > 2 else "N/A"
                top5.append({
                    "rank": rank,
                    "name": name,
                    "points": points
                })
            else:
                logging.warning(f"Skipping row with insufficient columns: {cols}")
        
        return top5
    
    except Exception as e:
        logging.error(f"Error scraping Serbian rankings: {e}")
        return []

# For testing
if __name__ == "__main__":
    for player in get_top5():
        print(f"Rank: {player['rank']}, Name: {player['name']}, Points: {player['points']}")
