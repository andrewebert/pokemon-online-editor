GENERATIONS = ["1G", "2G", "3G", "4G", "5G"]
EXTENSION = ".txt"
import csv

def flatten(ls):
    return [item for sublist in ls for item in sublist]

def invert_dict(d):
    return dict(zip(d.values(), d.keys()))

def lines(f):
    return [str(line).strip() for line in f]

def lines_dict(filename):
    with open(filename + EXTENSION) as f:
        return dict(enumerate(lines(f)))

# Get the names of all the types from the types folder
type_names = lines_dict("../types/types")
move_names = lines_dict("../moves/moves")
ability_names = lines_dict("../abilities/abilities")

def write_csv(filename, table):
    with open(filename + ".csv", "wb") as f:
        csv.writer(f).writerows(table)

# Add a number of columns to the table based on a list of file-conversion dict pairs
# and a function for processing lines in the file
def add_columns(table, folder, files, linefunc=None):
    [add_column(table, folder, filename, conversion, linefunc)
        for filename, conversion in files]

def add_column(table, folder, filename, conversion, linefunc=None):
    table[0].append(filename)
    with open(folder + "/" + filename + EXTENSION) as f:
        # extract the data from the file
        column = lines(f)
    for i in range(len(column)):
        # if the data needs to be extracted from the line
        # (e.g. pokemon number removed), do so
        entry = column[i]
        if linefunc != None:
            entry = linefunc(entry)
        # convert the data from a number to a word if necessary
        if conversion != None:
            entry = conversion[int(entry)]
        table[i+1].append(entry)

