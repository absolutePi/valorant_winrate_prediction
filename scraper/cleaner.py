import csv
import re

def extract_first_number(field):
    # Use regular expression to extract the first number from the field
    match = re.match(r'^([\d\.]+)', field)
    if match:
        return match.group(1)
    else:
        return None


with open('cleaned_player_stats.csv', 'w', newline='', encoding='utf-8') as cleaned_stats:
    cleaned_writer = csv.writer(cleaned_stats)
    cleaned_writer.writerow(['name/org', 'rating', 'acs', 'k/d/a', 'drop', 'drop1', 'kill-death', 'kast%', 'adr',
                              'hs%', 'fk/fd/diff', 'drop2', 'drop3'])
    with open('player_stats.csv', 'r', newline='', encoding='utf-8') as uncleaned_stats:
        file1 = csv.reader(uncleaned_stats)
        next(file1)
        for line in file1:
            new_line = []
            for idx, field in enumerate(line):
                if idx == 0 or idx == 4 or idx == 6 or idx == 7:  # Skip cleaning for specific indices
                    new_line.append(field)  # Append as is
                else:
                    cleaned_field = extract_first_number(field)
                    new_line.append(cleaned_field)


            cleaned_writer.writerow(new_line)