import csv

opStatus = csv.writer(open('analysis2.csv', 'w'), delimiter = ',', quotechar = '"')

for i in range(1, 251):
    inpStatus = csv.reader(open('analysis3.csv','r'), delimiter = ',', quotechar='"')
    statuses = ""
    for row in inpStatus:
        break
    for row in inpStatus:
        sn = int(row[0])
        status = row[2]
        if sn == i:
            userid = row[1]
            statuses += status + "#####"
            ext = row[3]
            neu = row[4]
            agr = row[5]
            con = row[6]
            opn = row[7]
            e = row[8]
            n = row[9]
            a = row[10]
            c = row[11]
            o = row[12]
    opStatus.writerow([userid, statuses, opn, o, con, c, ext, e, agr, a, neu, n])
