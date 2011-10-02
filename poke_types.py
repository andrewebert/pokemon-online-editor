# Converts all the information about types to a csv file
from util import *

TYPES = "../types/"
NEW_FOLDER = "new/types/"

def to_csv(generation="5G"):
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
    write_csv("types/types", table)

def from_csv(generation="5G"):
    # Read the csv
    table = read_csv("types/types")

    # Construct type names, ignoring blank first entry
    with open(NEW_FOLDER + 'types.txt', 'wb') as f:
        names = table[0][1:]
        f.write("\n".join(names));

    # Construct unlabled type effectiveness table
    with open(NEW_FOLDER + 'typestable.txt', 'wb') as f:
        effectiveness = [row[1:] for row in table[1:]]
        f.write("\n".join([" ".join(row) for row in effectiveness]) + "\n")
