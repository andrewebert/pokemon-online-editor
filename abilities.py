# Converts abilities to csv

from util import *

ABILITIES = "../abilities/"
NEW_FOLDER = "new/abilities/"

def to_csv(generation="5G"):
    table = [[]]
    add_columns(table, ABILITIES, [
        ("abilities",                       None),
        ("ability_desc",                    None),
        ("ability_effects_" + generation,   None),
        ("ability_battledesc",              None)
    ])
    #add_column(table, ABILITIES, "ability_messages", separator="|")
    write_csv("abilities/abilities", table)

def from_csv(generation="5G"):
    csv_to_txt("abilities/abilities", NEW_FOLDER)
