import csv
filename = 'D:/Google Drive/data2/barf.csv'
ifile = open(filename, "r")
reader = csv.reader(ifile)
for row in reader:
    if len(row) > 1:
        if row[1].lstrip() == "XXX":
            break
