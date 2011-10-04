GENERATIONS = ["1G", "2G", "3G", "4G", "5G"]
EXTENSION = ".txt"
import csv

def flatten(ls):
    return [item for sublist in ls for item in sublist]

def invert_dict(d):
    return dict(zip(d.values(), d.keys()))

def lines(filename):
    with open(filename) as f:
        return [str(line).strip() for line in f]

def lines_dict(filename):
    return dict(enumerate(lines(filename + EXTENSION)))

# Get the names of all the types from the types folder
type_names = lines_dict("../types/types")
move_names = lines_dict("../moves/moves")
ability_names = lines_dict("../abilities/abilities")

def write_csv(filename, table):
    with open(filename + ".csv", "wb") as f:
        csv.writer(f).writerows(table)

def read_csv(filename):
    with open(filename + ".csv", "r") as f:
        return [line for line in csv.reader(f)]

def csv_to_txt(filename, new_folder):
    write_txt(new_folder, read_csv(filename))

def write_txt(new_folder, table):
    for j, header in enumerate(table[0]):
        with open(new_folder + header + EXTENSION, 'wb') as f:
            f.write("\n".join([row[j] for row in table[1:] if j < len(row)]))

# Add a number of columns to the table based on a list of file-conversion dict pairs
# and a function for processing lines in the file
def add_columns(table, folder, files, linefunc=None):
    [add_column(table, folder, filename, conversion, linefunc)
        for filename, conversion in files]

def add_column(table, folder, filename, conversion=None, linefunc=None, separator=None):
    table[0].append(filename)
    # extract the data from the file
    column = lines(folder + "/" + filename + EXTENSION)
    for i in range(len(column)):
        # if the data needs to be extracted from the line
        # (e.g. pokemon number removed), do so
        entry = column[i]
        if linefunc != None:
            entry = linefunc(entry)
        # convert the data from a number to a word if necessary
        if conversion != None:
            entry = conversion[int(entry)]
        # if there are multiple columns to be added, split the data into columns
        if separator != None:
            entry = entry.split(separator)
        else:
            entry = [entry]
        # if this is the first column, add an extra row for the data if necessary
        if len(table) <= i+1:
            table.append([])
        table[i+1] += entry

