import csv
with open("existing.csv", "r") as f:
    reader = csv.reader(f)
    sum = 0
    count = 0
    for row in reader:
        sum += float(row[4])
        count += 1
    print(sum / count)
with open("existing.csv", "r") as f:
    reader = csv.reader(f)
    sum = 0
    count = 0
    for row in reader:
        sum += float(row[5])
        count += 1
    print(sum / count)