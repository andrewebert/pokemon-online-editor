import csv
from util import *

MOVES = "../moves/"
CSV_FOLDER = "moves/"
NEW_FOLDER = "new/moves/"
MAX_CAUSED_EFFECTS = 50 # Actually 21, but there's no harm in guessing high

# Damage class names
damage_names = {
    0: "none", 
    1: "physical", 
    2: "special"
}

# Names of caused effects (poison, paralysis, etc). Complicated status
# is listed as other.
caused_effect_names = lines_dict("../status/status")
for i in range(len(caused_effect_names), MAX_CAUSED_EFFECTS+1):
    caused_effect_names[i] = "Special(" + str(i) + ")"
caused_effect_names[-1] = "Other"

FILES = [
    ("type",            type_names),
    ("damage_class",    damage_names),
    ("pp",              None),
    ("power",           None),
    ("accuracy",        None),
    ("priority",        None),
    ("effect",          None),
    ("effect_chance",   None),
    ("caused_effect",   caused_effect_names),
    ("crit_rate",       None),
    ("recoil",          None),
    ("flinch_chance",   None),
    ("healing",         None),
    ("min_turns",       None),
    ("max_turns",       None),
    ("status",          None),
    ("category",        None),
    ("range",           None),
    ("flags",           None),
    ("None0",           None),
    ("None1",           None),
    ("None2",           None),
    ("padding0",        None),
    ("padding1",        None),
    ("padding2",        None)
]

def to_csv(generation="5G"):
    # Get the names of all the moves
    with open(MOVES + "moves.txt") as f:
        table = [["id", "name"]] + [[i, name] for i, name in enumerate(lines(f))]

    # Open the files and add their content to the table. Each file represents
    # one column, in order. There is a conversion dictionary to convert from
    # numbers to names.
    add_columns(table, MOVES + generation, FILES)
    
    # Write the table to a csv file
    write_csv("moves/moves", table)

def from_csv(generation="5G"):
    table = read_csv("moves/moves")

    # Get the conversion dictionaries
    conversions = dict(FILES)
    conversions["name"] = None

    # Write the results of each column to a separate file
    for j, name in enumerate(table[0][1:]):
        if j == 0:
            filename = "moves.txt"
        else:
            filename = generation + "/" + name + EXTENSION
        
        conversion_dict = conversions[name] 
        if conversion_dict == None:
            column = [row[j+1] for row in table[1:]]
        else:
            column = [str(invert_dict(conversion_dict)[row[j+1]]) for row in table[1:]]

        with open(NEW_FOLDER + filename, "wb") as f:
            f.write("\n".join(column))
