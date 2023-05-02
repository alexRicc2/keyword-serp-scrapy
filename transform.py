import csv
filename = 'new.txt'

with open(filename, 'r') as file:
    lines = file.readlines()


with open('keywordsOnly.csv', 'w', newline='') as output:
  writer = csv.writer(output)
  for idx, line in enumerate(lines):
      keyword = line.split('"')[1]
      writer.writerow([keyword])