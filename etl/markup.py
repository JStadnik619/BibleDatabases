"""
POC for using usfm-grammar instead of implementing my own USFM parser.
Based on https://github.com/Bridgeconn/usfm-grammar/tree/master/py-usfm-parser
"""

import os
import csv

# TODO: Use a subset of this code instead of importing the whole package
from usfm_grammar import USFMParser, Filter


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
source_directory = os.path.join(base_dir, 'sources')
gen_usfm = os.path.join(source_directory, 'bsb_usfm/01GENBSB.SFM')
input_usfm_str = open(gen_usfm,"r", encoding='utf8').read()

my_parser = USFMParser(input_usfm_str)

# errors = my_parser.errors
# print(errors)

list_output = my_parser.to_list() 
#list_output = my_parser.to_list([Filter.SCRIPTURE_TEXT])

# table_output = "\n".join([",".join(row) for row in list_output])

with open(os.path.join(base_dir, 'databases/gen.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(list_output)

# TODO: Save list output to SQLite markup table
