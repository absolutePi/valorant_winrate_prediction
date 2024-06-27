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
    cleaned_writer.writerow(['name', "empty", 'rating', 'acs', 'k', 'd', 'a', 'drop', 'drop1', 'kill-death', 'kast%', 'adr',
                             'hs%', 'fk/fd/diff', 'drop2', 'drop3', 'org'])
    with open('player_stats.csv', 'r', newline='', encoding='utf-8') as uncleaned_stats:
        file1 = csv.reader(uncleaned_stats)
        next(file1)
        for line in file1:
            new_line = []
            for idx, field in enumerate(line):
                if idx == 0 or idx == 6 or idx == 7 or idx == len(line)-1:  # Skip cleaning for specific indices
                    new_line.append(field)  # Append as is
                elif idx == 4:
                    kda = line[4]
                    k = line[4][0:2]
                    d = line[4][3:len(line[4]) - 3]
                    a = line[4][len(line[4]) - 3:len(line[4]) - 1]
                    new_line.append(k)
                    new_line.append(d)
                    new_line.append(a)
                else:
                    cleaned_field = extract_first_number(field)
                    new_line.append(cleaned_field)


            cleaned_writer.writerow(new_line)


player_stats = pd.read_csv('cleaned_player_stats.csv', skipinitialspace=True)
player_stats.columns = player_stats.columns.str.strip()
try:
    player_stats.drop('drop3', inplace=True, axis=1)
    player_stats.drop('drop2', inplace=True, axis=1)
    player_stats.drop('drop1', inplace=True, axis=1)
    player_stats.drop('drop', inplace=True, axis=1)
    player_stats.drop('empty', inplace=True, axis=1)
except KeyError:
    pass
print(player_stats)
player_stats.to_csv('cleaned_player_stats.csv', index_label=False)

