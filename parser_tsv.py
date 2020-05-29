import csv
from db_request import insert_music

array_music = []
unic_nconst = set()
with open('data/name.basics.tsv', newline='') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    countrow = 0
    for row in reader:
        prof = row['primaryProfession'].strip(" ").split(",")
        if 'composer' in prof or 'soundtrack' in prof:
            if row['nconst'] not in unic_nconst:
                insert_row = [int(row['nconst'][2:]), row['nconst'], row['primaryName'], row['primaryProfession'],row['knownForTitles'] ]
                array_music.append(insert_row)
                unic_nconst.add(row['nconst'])
                countrow += 1

print(countrow)
insert_music(array_music)

