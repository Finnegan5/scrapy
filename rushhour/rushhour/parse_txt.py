import json
import csv
import re
from collections import ChainMap


ids=[]
with open('rush.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if not row[2] == 'id': ids.append(row[2])


with open('rush_prices.json') as json_file:
    data = json.load(json_file)
    result = dict(ChainMap(*data))
    for id in ids:
        x = re.search('\d+,\d\d' ,result[id])
        result[id] = x.group(0)

with open('rush_out.csv', 'w') as csv_out:
    writer = csv.writer(csv_out, delimiter=',', quotechar='"')

    with open('rush.csv') as csv_file2:
        reader2 = csv.reader(csv_file2, delimiter=',')

        for row in reader2:
            if not row[2] == 'id': row[2] = result[row[2]].replace(',', '.')
            writer.writerow(row)


