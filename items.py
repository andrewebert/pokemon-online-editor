# Converts items to csv
from util import *

ITEMS = "../items/"
NEW_FOLDER = "new/items/"

def to_csv(generation="5G"):
    item_table = [[]]
    add_columns(item_table, ITEMS, [
        ("items",                       None),
        ("item_useful",                 None),
        ("item_effects_" + generation,  None),
        ("items_description",           None)
    ])
    write_csv("items/items", item_table)
    
    berry_table = [[]]
    add_columns(berry_table, ITEMS, [
        ("berries",                     None),
        ("berry_pow",                   None),
        ("berry_type",                  None),
        ("berry_effects",               None),
        ("berries_description",         None)
    ])
    write_csv("items/berries", berry_table)

def from_csv(generation="5G"):
    csv_to_txt("items/items", NEW_FOLDER)
    csv_to_txt("items/berries", NEW_FOLDER)
