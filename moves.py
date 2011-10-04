import csv
from util import *
from enums import *

MOVES = "../moves/"
CSV_FOLDER = "moves/"
NEW_FOLDER = "new/moves/"
MAX_CAUSED_EFFECTS = 50 # Actually 21, but there's no harm in guessing high

# Names of caused effects (poison, paralysis, etc). Complicated status
# is listed as other.
caused_effect_names = lines_dict("../status/status")
for i in range(len(caused_effect_names), MAX_CAUSED_EFFECTS+1):
    caused_effect_names[i] = "Special(" + str(i) + ")"
caused_effect_names[-1] = "Other"

stat_names2 = stat_names
stat_names2[0] = ""

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
    ("category",        category_names),
    ("crit_rate",       None),
    ("recoil",          None),
    ("flinch_chance",   None),
    ("healing",         None),
    ("min_turns",       None),
    ("max_turns",       None),
    ("status",          status_kind_names),
    ("range",           range_names),
    #("flags",           None),
    #("None0",           None),
    #("None1",           None),
    #("None2",           None),
]

def to_csv(generation="5G"):
    # Get the names of all the moves
    table = [["id", "name"]] + [[i, name] for i, name in enumerate(lines(MOVES + "moves.txt"))]

    # Open the files and add their content to the table. Each file represents
    # one column, in order. There is a conversion dictionary to convert from
    # numbers to names.
    add_columns(table, MOVES + generation, FILES)

    # Deal with stat boosts
    stat_affected = lines(MOVES + generation + "/None0.txt")
    stat_boosts = lines(MOVES + generation + "/None1.txt")
    stat_chance = lines(MOVES + generation + "/None2.txt")

    # Splits a 6-digit hexadecimal number into three 2-digit hexadecimal
    # numbers
    def split(n):
        return [n/pow(16,4), (n % pow(16,4))/pow(16,2), n % pow(16,2)]

    # Extract the stat boost data from the None*.txt files
    [stat_affected, stat_boosts, stat_chance] =\
        [[split(int(line)) for line in stat_file]
        for stat_file in [stat_affected, stat_boosts, stat_chance]]
    
    # Get the names of the stats affected
    stat_affected = [[stat_names2[x] for x in triple] 
            for triple in stat_affected]

    # Negative boosts are represented by large whole numbers, change this
    stat_boosts = [[x if x < 126 else (x - 256) for x in triple]
            for triple in stat_boosts]

    for j in range(3):
        table[0] += ["stat" + str(j) + s for s in ["", " stages", " chance"]]
    for i in range(len(stat_affected)):
        for j in range(3):
            for l in [stat_affected, stat_boosts, stat_chance]:
                table[i+1].append(l[i][j])

    # Deal with flags
    table[0].append("flags")
    flags = [int(l) for l in lines(MOVES + generation + "/flags.txt")]
    for i, flag in enumerate(flags):
        for n, flag_name in flag_names.items():
            if (flag % (2*n))/n == 1:
                table[i+1].append(flag_name)

    # Write the table to a csv file
    write_csv("moves/moves", table)

def from_csv(generation="5G"):
    table = read_csv("moves/moves")
    headers = table[0]
    data = table[1:]
    new_folder = NEW_FOLDER + generation + "/" 

    # Get the conversion dictionaries
    conversions = dict(FILES)
    conversions["name"] = None

    # Rename the moves row
    table[0][1] = "moves"
    # Find out where the stats row is
    s = headers.index("stat0")

    # Perform conversions on all columns except "id"
    # and the stats and flags columns
    for j, name in enumerate(headers[1:s]):
        if j == 0:
            conversion_dict = None
        else:
            conversion_dict = conversions[name]

        if conversion_dict == None:
            column = [row[j+1] for row in data]
        else:
            column = [str(invert_dict(conversion_dict)[row[j+1]]) 
                for row in data]

        with open(new_folder + name + EXTENSION, "wb") as f:
            f.write("\n".join(column))

    # Deal with stat changes
    def to_int(x):
        return 0 if x == "" else int(x)
    convert_functions = {
        0: (lambda x: to_int(invert_dict(stat_names2)[x])),
        1: (lambda x: to_int(x) if to_int(x) >= 0 else to_int(x) + 256),
        2: to_int
    }
    # Get the stats from the CSV and convert it into a list where each row
    # is of the form
    # [
    #   [stat0, stat1, stat2], 
    #   [stat0_boost, stat1_boost, stat2_boost],
    #   [stat0_stages, stat1_stages, stat2_stages]
    # ]
    # where stat0, etc are integers
    stats = [ [[convert_functions[i](row[s+i+3*j])
            for j in range(3)] 
            for i in range(3)]
            for row in data ]
    
    # Convert each triple [0,1,2] into a single integer, then convert
    # that integer into a string
    stats = [[str(sum([pow(16,2*(2-i)) * t for i, t in enumerate(triple)]))
        for triple in row]
        for row in stats]

    # Add headers to the stats table
    stats.insert(0, ["None0", "None1", "None2"])

    # Write stats to files
    write_txt(new_folder, stats)
     
    # Get the flags from the file
    s = headers.index("flags")
    flags = [row[s:] for row in data]
    flags = [str(sum([invert_dict(flag_names)[f] 
        for f in row])) 
        for row in flags]
    
    with open(new_folder + "flags.txt", "wb") as f:
        f.write("\n".join(flags))
    
