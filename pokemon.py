# Converts pokemon data to CSV
# WARNING: some data about pokemon ablities is not visible in the CSVs.
# There are abilities listed for pokemon with numbers 650-667, but no pokemon
# with those numbers. This data is stored in extra_abilities.csv.

import os
import glob
from util import *

POKEMON = "../pokes/"
ERRONEOUS_FILES = ["poke_weight"]
NUMBER_REPLACE = {"01:0":"1:0","02:0":"2:0","03:0":"3:0","04:0":"4:0",
    "05:0":"5:0", "06:0":"6:0","07:0":"7:0","08:0":"8:0","09:0":"9:0"}
MAX_POKEMON_NUMBER = 649
EXCESS = "ex_"
EXCESS_FILES = ["poke_ability1_5G", "poke_ability2_5G", "poke_ability3_5G"]

STAT_LABELS = ["hp", "attack", "defense", "special attack", 
    "special defense", "speed"]

COMBINATIONS_FILES = [kind + gen 
        for kind in ["event_combinations_", "legal_combinations_"]
        for gen in GENERATIONS
        # There's no legal_combinations_1G.txt file
        if not (kind == "legal_combinations_" and gen == "1G")]

type_names2 = type_names
type_names2[17] = ""

# Sorts a list of pokemon numbers, represented as strings
def pokemon_sort(pokes):
    return [t[1] for t in sorted([(map(int, pokemon.split(':')[:2]), (pokemon, data)) 
        for pokemon, data in pokes])]

def get_type_files(generation):
    # Replace "???" for no type with a blank
    return [
        ("poke_type1-" + generation,   type_names2),
        ("poke_type2-" + generation,   type_names2)
    ]

# Generations 1 and 2 have no abilities
# Generations 3 and 4 have two abilities
# Generation 5 has three abilities
def get_ability_files(generation):
    if not generation in ["3G", "4G", "5G"]:
        return []
    files = [
        ("poke_ability1_" + generation, ability_names),
        ("poke_ability2_" + generation, ability_names)
    ]
    if generation == "5G":
        files.append(("poke_ability3_5G", ability_names))
    return files

def second(s):
    return s.split(" ")[1]

def add_entry(tables, folder, filename, conversion):
    with open(folder + filename + EXTENSION) as f:
        for line in lines(f):
            (no, _, entry) = line.partition(" ")
            # For some reason poke_weight lists the pokemon numbers incorrectly.
            if filename in ERRONEOUS_FILES:
                if no in NUMBER_REPLACE:
                    no = NUMBER_REPLACE[no]
            # The 5G ability files give abilities to unnumbered pokemon, and miss some
            # alternate formes. I don't know what's going on here. Abilities for
            # unknown pokemon are placed in excess data files and copied back when
            # the csvs are converted to txt files.
            if int(no.split(':')[0]) > MAX_POKEMON_NUMBER:
                with open("pokemon/" + EXCESS + filename + EXTENSION, 'a') as ex_f:
                    ex_f.write(line + "\n")
            else:
                # Perform the conversion if necessary
                if conversion != None:
                    entry = conversion[int(entry)]
                # Add the label and data
                tables[no].append([filename, entry])

def get_table(tables, filename):
    with open(POKEMON + filename + EXTENSION) as f:
        for line in lines(f):
            data = line.split(" ")
            table = tables[data[0]]
            data = data[1:]
            yield (table, data)

# Format
# Bulbasaur.csv:
#   id, 1
#   no, 1:0
#   name, Bulbasaur
#   attack, 43
#   ...
#   5G_level_moves, move1, move2, move3
def to_csv(generation="5G"):
    # Clear the excess data files and number replacement files
    for filename in EXCESS_FILES:
        with open("pokemon/" + EXCESS + filename + EXTENSION, "w") as f:
            f.write("");
    with open("pokemon/number_replacements.txt", "w") as f:
        f.write("");

    tables = {}

    with open(POKEMON + "pokemons.txt") as f:
        for line in lines(f):
            (number, _, name) = line.partition(" ")
            # Ignore any annotation after the sub-number (e.g. H for arceus)
            numbers = number.split(":")
            if len(numbers) > 2:
                new_number = numbers[0] + ":" + numbers[1]
                # If we've changed the pokemon number, make a note of it
                with open("pokemon/number_replacements.txt", "a") as f:
                    f.write(new_number + " " + number + "\n")
            else:
                new_number = number
            tables[new_number] = [["no", new_number], ["pokemons", name]]
    
    # Add the types and abilities
    for filename, conversion in get_type_files(generation)\
            + get_ability_files(generation):
        add_entry(tables, POKEMON, filename, conversion)

    # Get the pokemon stats, which are all stored in one file
    for (table, data) in get_table(tables, "poke_stats"):
        table += [[label, stat] for (label, stat) in zip(STAT_LABELS,
            [int(n) for n in data])]

    # Get the names of all the files containing pokemon moves
    moves_files = [gen + "_" + kind + "_moves"
        for gen in GENERATIONS
        for kind in ["egg", "level", "pre_evo", "special", "tm_and_hm", "tutor"]]
    # Each file represents a row in the table of that pokemon
    for filename in moves_files:
        for (table, data) in get_table(tables, filename):
            table.append([filename] + [move_names[int(move)] for move in data])

    # Move combinations (| separated)
    for filename in COMBINATIONS_FILES:
        for (table, data) in get_table(tables, filename):
            # Undo the separation done by get_table
            data = " ".join(data)
            # Different event combinations for the same pokemon are split by "|"
            # Each event combination consists of a space-separated list of move
            # numbers.
            for i, entry in enumerate(data.split("|")):
                table.append([filename + "_" + str(i)] + 
                    [move_names[int(move)] for move in entry.split(" ")])

    # Add irrelevant crap
    reverse_generation = {"1G":"G1", "2G":"G2", "3G":"G3", "4G":"G4", "5G":"G5"}[generation]
    for filename, conversion in [
            ("minlevels_" + reverse_generation, None),
            ("poke_weight",                     None),
            ("height",                          None),
            ("poke_gender",                     None) ] :
        add_entry(tables, POKEMON, filename, conversion) 

    # Currently missing: classification, cries, description, evolutions,
    # gender rate, level balance
    # None of this is particulary relevant; the text files for them are formatted
    # unusually and are hard to parse.

    # Write the tables to csv files
    for table in tables.values():
        name = table[1][1]
        write_csv("pokemon/" + name, table)

def from_csv(generation="5G"):
    tables = {}
    pokemon = set()
    for filename in glob.glob(os.path.join("pokemon/", "*.csv")):
        print "reading", filename
        # read_csv adds the .csv extension, so we need to remove it from filename
        table = read_csv(filename[:-4])
        number = table[0][1]
        pokemon.add(number)
        for line in table[1:]:
            label = line[0]
            data = line[1:]
            # Create the table for the label if it doens't already exist
            if not label in tables:
                tables[label] = {}

            # Modify the data to get it back to its original format
            if "poke_type" in label:
                data = str(invert_dict(type_names2)[data[0]])
            elif "poke_ability" in label:
                data = str(invert_dict(ability_names)[data[0]])
            elif "moves" in label or "combinations" in label:
                data = " ".join([str(invert_dict(move_names)[e]) for e in data])
            else:
                # Default data format is a single element
                data = str(data[0])

            tables[label][number] = data
    
    # Gets the stats of all pokemon, condensing them into a string
    # Ignore alternate formes which don't have separate stats listed
    stats = dict([(poke, 
        " ".join([tables[stat][poke] for stat in STAT_LABELS])
        ) for poke in pokemon if poke in tables["hp"]])
    # Replace the tables for individual stats with one table for all stats
    tables["poke_stats"] = stats
    for stat in STAT_LABELS:
        tables.pop(stat)

    # Convert the combinations files to '|'-separated lists of combinations
    for filename in COMBINATIONS_FILES:
        tables[filename] = {}
        labels = [label for label in tables if filename in label]
        combinations = [tables[label] for label in labels]
        for poke in pokemon:
            combination = [c[poke] for c in combinations if poke in c]
            if combination != []:
                combination = '|'.join(combination)
                tables[filename][poke] = combination
        # Get rid of the excess table labels
        for label in labels:
            tables.pop(label)
    
    # Add annotations to the pokemon numbers in pokemons.txt
    with open("pokemon/number_replacements.txt", "r") as f:
        for old, new in [line.strip().split(" ") for line in f]:
            tables["pokemons"][new] = tables["pokemons"].pop(old)

    # Modify the pokemon numbers in poke_weight.txt
    weight = tables["poke_weight"]
    rev = invert_dict(NUMBER_REPLACE)
    for poke, data in weight.items():
        if poke in rev:
            weight[rev[poke]] = weight.pop(poke)

    # Finally, write out all the data to csv files
    for filename, table in tables.items():
        #print filename
        with open("new/pokemon/" + filename + ".txt", 'wb') as f:
            for pokemon, data in pokemon_sort(table.items()):
                f.write(pokemon + " " + data + "\n")

    # Write out the excess pokemon abilities
    for filename in EXCESS_FILES:
        with open("pokemon/" + EXCESS + filename + EXTENSION, "r") as f:
            with open("new/pokemon/" + filename + EXTENSION, "a") as g:
                g.write("\n".join([l.strip() for l in f]))


    
            
            
                


                

