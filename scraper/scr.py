from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrape_match_stats(match_url):
    print(f"Accessing URL: {match_url}")
    driver.get(match_url)

    try:
        # Wait until the player stats container is present
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vm-stats-container"))
        )
        print("Player stats container located.")
        time.sleep(10)  # Allow extra time for table to load

        # Scroll down to ensure all content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Parse page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Debug output to verify the page source
        with open("page_source.html", "w", encoding='utf-8') as file:
            file.write(str(soup.prettify()))

        # Locate both teams' stats tables
        team_stats_tables = soup.find_all('table', class_='wf-table-inset mod-overview')
        match_stats = []

        if team_stats_tables and len(team_stats_tables) >= 2:
            for table in team_stats_tables:
                rows = table.find_all('tr')

                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all('td')
                    player_data = [col.get_text(separator="\n").strip() for col in cols]
                    match_stats.append(player_data)

            print("Player stats tables found and parsed.")
        else:
            print("Player stats tables not found or incomplete.")

        # Scrape the scores
        scores = soup.find_all('div', class_='score')
        score_list = [score.get_text().strip() for score in scores]
        print("Scores found and parsed.")
        
        return match_stats, score_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []

# Example match URL
match_url = "https://www.vlr.gg/353178/sentinels-vs-nrg-esports-champions-tour-2024-americas-stage-2-w1"

# Use the function to scrape player stats and scores
match_stats, scores = scrape_match_stats(match_url)

# Clean and structure the player stats data
cleaned_stats = []
for stats in match_stats:
    # Clean each element by removing unnecessary characters
    cleaned_stats.append([stat.replace("\n", " ").strip() for stat in stats])

# Print the cleaned player stats
print("\nCleaned Player Stats:")
for stats in cleaned_stats:
    print(stats)

# Print the scores
print("\nScores:")
for score in scores:
    print(score)

# Clean up
driver.quit()
