import csv
import re
import pandas as pd

def extract_first_number(field):
    # Use regular expression to extract the first number from the field
    match = re.match(r'^([\d\.]+)', field)
    if match:
        return match.group(1)
    else:
        return None


with open('cleaned_player_stats.csv', 'w', newline='', encoding='utf-8') as cleaned_stats:
    cleaned_writer = csv.writer(cleaned_stats)
    cleaned_writer.writerow(['name', "empty", 'rating', 'acs', 'k', 'd', 'a', 'k-d', 'kast%', 'adr', 'hs%',
                             'fk', 'fd', 'fd/fd/diff', 'org'])
    with open('player_stats.csv', 'r', newline='', encoding='utf-8') as uncleaned_stats:
        file1 = csv.reader(uncleaned_stats)
        next(file1)
        for line in file1:
            new_line = []
            for idx, field in enumerate(line):
                if idx == 0 or idx == len(line):  # Skip cleaning for specific indices
                    new_line.append(field)  # Append as is
                elif idx == 4:
                    kills = line[4][0:2].strip(" ")
                    new_line.append(kills)
                elif idx == 5:
                    deaths = line[5][6:9].strip(" ")
                    new_line.append(deaths)
                elif idx == 6:
                    assists = line[6][:3].strip(" ")
                    new_line.append(assists)
                elif idx == 7:
                    diff = line[7][:3]
                    new_line.append(diff)
                    #print(diff)
                elif idx == 8:
                    kast = line[8][:3].strip("%")
                    new_line.append(kast)
                elif idx == 13:
                    fk = line[11][0:3]
                    fd = line[12][0:3]
                    fk_fd = int(fk)-int(fd)
                    #print(fk_fd)
                    #print(fk_fd_diff)
                    new_line.append(fk_fd)
                elif idx == len(line)-1:
                    new_line.append(line[len(line)-1])
                else:
                    cleaned_field = extract_first_number(field)
                    new_line.append(cleaned_field)


            cleaned_writer.writerow(new_line)


player_stats = pd.read_csv('cleaned_player_stats.csv', skipinitialspace=True)
player_stats.columns = player_stats.columns.str.strip()
try:
    #player_stats.drop('drop1', inplace=True, axis=1)
    #player_stats.drop('drop', inplace=True, axis=1)
    player_stats.drop('empty', inplace=True, axis=1)
except KeyError:
    pass
#print(player_stats)
player_stats.to_csv('cleaned_player_stats.csv', index=False)

match_scores = []
with open("cleaned_match_scores.csv", 'w') as cleaned_stats:
    csvwriter = csv.writer(cleaned_stats)
    csvwriter.writerow(["Win/Loss"])
    with open("match_scores.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for i in csvreader:
            match_scores.append(i)


#combined player stats
match_scores = []
with open("cleaned_match_scores.csv", 'w') as cleaned_stats:
    csvwriter = csv.writer(cleaned_stats)
    csvwriter.writerow(["Win/Loss"])
    with open("match_scores.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for i in csvreader:
            match_scores.append(i)
    #print(match_scores, "\n")
    for idx, i in enumerate(match_scores):
        if idx % 2 == 0:
            team1, team2 = int(str(match_scores[idx]).strip("''[]")), int(str(match_scores[idx + 1]).strip("''[]"))
            if team1 > team2:
                team1 = ['win']
                team2 = ['lose']
            else:
                team1 = ['lose']
                team2 = ['win']
            for i in range(0,5):
                csvwriter.writerow(team1)
            for j in range(0,5):
                csvwriter.writerow(team2)

results = []
with open("combined_stats.csv", 'w') as combined:
    csvwriter = csv.writer(combined)
    csvwriter.writerow(['name', 'rating', 'acs', 'k', 'd', 'a', 'k-d', 'kast%', 'adr', 'hs%',
                             'fk', 'fd', 'fd/fd/diff', 'org', 'result'])
    with open("cleaned_player_stats.csv", 'r') as csvfile2:
        csvreader2 = csv.reader(csvfile2)
        next(csvreader2)
        with open("cleaned_match_scores.csv", 'r') as csvfile3:
            csvreader3 = csv.reader(csvfile3)
            next(csvreader3)
            for i in csvreader3:
                results.append(i)
            for idx, line in enumerate(csvreader2):
                try:
                    result_to_be_added = (str(results[idx]).strip("''[]"))
                    line.append(result_to_be_added)
                    csvwriter.writerow(line)
                except IndexError:
                    print("Mismatch between number of stats recorded")

#average stats for teams
with open("combined_team_stats.csv", "w") as csvfile2:
    csvwriter = csv.writer(csvfile2)
    csvwriter.writerow(
        ["org", "result", "avg_rating", "avg_acs", "k", "d", "a", "k-d", "avg_kast%", "avg_adr", "avg_hs%", "fk", "fd", "fk-fd"])
    with open("combined_stats.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        ind_stats = []
        for line in csvreader:
            ind_stats.append(line)
        for idx, record in enumerate(ind_stats):
            if idx % 5 == 0:
                new_line = []
                new_line.append(record[13])
                new_line.append(record[14])
                for idx1, data in enumerate(record):
                    if idx1 == 1 or idx1 == 2 or idx1 == 7 or idx1 == 8 or idx1 == 9:
                        new_data = (float(ind_stats[idx][idx1]) + float(ind_stats[idx + 1][idx1]) + float(
                            ind_stats[idx + 2][idx1]) + float(ind_stats[idx + 3][idx1]) + float(
                            ind_stats[idx + 4][idx1])) / 5
                        new_line.append(new_data)
                    if idx1 == 3 or idx1 == 4 or idx1 == 5 or idx1 == 6 or idx1 == 10 or idx1 == 11 or idx1 == 12:
                        new_data  = (float(ind_stats[idx][idx1]) + float(ind_stats[idx + 1][idx1]) + float(
                            ind_stats[idx + 2][idx1]) + float(ind_stats[idx + 3][idx1]) + float(
                            ind_stats[idx + 4][idx1]))
                        new_line.append(new_data)
                csvwriter.writerow(new_line)

