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
                             'hs%', 'fk', 'fd', 'fk/fd/diff', 'org'])
    with open('player_stats.csv', 'r', newline='', encoding='utf-8') as uncleaned_stats:
        file1 = csv.reader(uncleaned_stats)
        next(file1)
        for line in file1:
            new_line = []
            for idx, field in enumerate(line):
                if idx == 0 or idx == len(line)-1:  # Skip cleaning for specific indices
                    new_line.append(field)  # Append as is
                elif idx == 4:
                    kills = line[4]
                    k = line[4][0:2]
                    k = k.strip(" ")
                    new_line.append(k)
                elif idx == 5:
                    deaths = line[5]
                    d = line[5][6:9]
                    d = d.strip(" ")
                    new_line.append(d)
                elif idx == 6:
                    assists = line[6]
                    a = line[6][0:3]
                    a = a.strip(" ")
                    new_line.append(a)
                elif idx == 7:
                    diff = line[7][0:3]
                    new_line.append(diff)
                    print(diff)
                elif idx == 13:
                    fk = line[11][0:3]
                    fd = line[12][0:3]
                    fk_fd = int(fk)-int(fd)
                    print(fk_fd)
                    #print(fk_fd_diff)
                    new_line.append(fk_fd)
                else:
                    cleaned_field = extract_first_number(field)
                    new_line.append(cleaned_field)


            cleaned_writer.writerow(new_line)


player_stats = pd.read_csv('cleaned_player_stats.csv', skipinitialspace=True)
player_stats.columns = player_stats.columns.str.strip()
try:
    player_stats.drop('fk', inplace=True, axis=1)
    player_stats.drop('fd', inplace=True, axis=1)
    player_stats.drop('drop1', inplace=True, axis=1)
    player_stats.drop('drop', inplace=True, axis=1)
    player_stats.drop('empty', inplace=True, axis=1)
except KeyError:
    pass
print(player_stats)
player_stats.to_csv('cleaned_player_stats.csv', index_label=False)
