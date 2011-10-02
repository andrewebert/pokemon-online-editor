# Converts all the information about types to a csv file
import csv
from util import lines

TYPES = "../types/"

def lines(f):
    return [str(line).strip() for line in f]

def to_csv():
    # read type names
    with open(TYPES + 'types.txt') as f:
        types = lines(f)

    # read type effectiveness, put it into table format
    # [["",    type1, type2],
    #  [type1, 1,     2    ],
    #  [type2, 4,     2    ]]
    with open(TYPES + 'typestable.txt') as f:
        headers = [""] + types
        # effectiveness is a 2d array
        effectiveness = [line.split(" ") for line in lines(f)]

        table = [headers] +\
            [[types[attacker]] +\
                [effectiveness[attacker][defender]
                    for defender in range(len(effectiveness[attacker]))]
                        for attacker in range(len(effectiveness))]

        #print table

    # write the type effectiveness to a csv
    with open(TYPES + 'types.csv', 'wb') as f:
        typesWriter = csv.writer(f)
        typesWriter.writerows(table)

def from_csv():
    # Read the csv
    with open(TYPES + 'types.csv', 'r') as f:
        typesReader = csv.reader(f)
        table = [line for line in typesReader]

    # Construct type names, ignoring blank first entry
    with open(TYPES + 'new/types.txt', 'wb') as f:
        names = table[0][1:]
        f.write("\n".join(names));

    # Construct unlabled type effectiveness table
    with open(TYPES + 'new/typestable.txt', 'wb') as f:
        effectiveness = [row[1:] for row in table[1:]]
        f.write("\n".join([" ".join(row) for row in effectiveness]) + "\n")
