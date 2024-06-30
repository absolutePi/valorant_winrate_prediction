from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

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
                for i, row in enumerate(rows[1:]):
                    cols = row.find_all('td')
                    player_data = [col.get_text(separator="\n").strip() for col in cols]
                    #making the player data readable
                    player_data.append(player_data[0][9:])
                    player_data[len(player_data)-1] = player_data[len(player_data)-1].strip("\t")
                    player_data[0] = player_data[0][0:10].strip("\t")
                    match_stats.append(player_data)

            print("Player stats tables found and parsed.")
        else:
            print("Player stats tables not found or incomplete.")

        # Scrape the scores
        scores = soup.find_all('div', class_='score')
        score_list = [score.get_text().strip() for score in scores]
        print("Scores found and parsed.")

        for i in range(0,10):
            match_stats.remove(match_stats[10])
        return match_stats, score_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []


# Example match URLs
all_matches = [
    "https://www.vlr.gg/353178/sentinels-vs-nrg-esports-champions-tour-2024-americas-stage-2-w1",
    "https://www.vlr.gg/353180/loud-vs-evil-geniuses-champions-tour-2024-americas-stage-2-w1"
]

# Adjust headers as needed
with open("player_stats.csv", "a", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        [
            "Player Name",
            "ACS (Map 1)", "ACS (Map 2)", "ACS (Map 3)",
            "K (Map 1)", "K (Map 2)", "K (Map 3)",
            "D (Map 1)", "D (Map 2)", "D (Map 3)",
            "A (Map 1)", "A (Map 2)", "A (Map 3)",
            "K/D (Map 1)", "K/D (Map 2)", "K/D (Map 3)",
            "KPR (Map 1)", "KPR (Map 2)", "KPR (Map 3)",
            "HS% (Map 1)", "HS% (Map 2)", "HS% (Map 3)",
            "ADR (Map 1)", "ADR (Map 2)", "ADR (Map 3)",
            "FK (Map 1)", "FK (Map 2)", "FK (Map 3)",
            "FD (Map 1)", "FD (Map 2)", "FD (Map 3)",
            "+/- (Map 1)", "+/- (Map 2)", "+/- (Map 3)",
            "FK/FD (Map 1)", "FK/FD (Map 2)", "FK/FD (Map 3)", "Team"
        ])  # Adjust headers as needed

with open("match_scores.csv", "a", newline='', encoding='utf-8') as csvfile2:
    writer2 = csv.writer(csvfile2)
    writer2.writerow(["Team Score"])

# Loop all matches
for url in all_matches:
    match_url = url
    match_stats, scores = scrape_match_stats(match_url)

    # Clean and structure the player stats data
    cleaned_stats = []
    for stats in match_stats:
        # Clean each element by removing unnecessary characters
        cleaned_stats.append([stat.replace("\n", " ").strip() for stat in stats])

    # Write the cleaned player stats to a CSV file
    with open("player_stats.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for stats in cleaned_stats:
            writer.writerow(stats)

    # Write the scores to a CSV file
    with open("match_scores.csv", "a", newline='', encoding='utf-8') as csvfile2:
        writer2 = csv.writer(csvfile2)
        for score in scores:
            writer2.writerow(score.split('-'))  # Split scores by dash or appropriate delimiter

    print("\nCleaned Player Stats:")
    for stats in cleaned_stats:
        print(stats)

    print("\nScores:")
    for score in scores:
        print(score)
# Clean up
driver.quit()
