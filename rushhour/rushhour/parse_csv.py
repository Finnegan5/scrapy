import csv

ids=[]
with open('platten.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        ids.append('+' + row[2])

def chunks(list, n):
    for i in range(0, len(list), n):
        yield ids[i:i + n]

chunky = list(chunks(ids, 600))

print(chunky[1])
url = 'https://www.rushhour.nl/index.php?q=rushhour/record/multiple/add-to-cart&nids='
string = ''.join(chunky[1]).replace("+id+", "")
print(url + string)
