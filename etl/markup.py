"""
POC for using usfm-grammar instead of implementing my own USFM parser.
Based on https://github.com/Bridgeconn/usfm-grammar/tree/master/py-usfm-parser
"""

import os
import csv

# TODO: Use a subset of this code instead of importing the whole package
from usfm_grammar import USFMParser, Filter


def format_records(records):
    """
    Convert column labels to lowercase and removing trailing whitespace from
    the text column.

    Args:
        records (list): a list of lists containing column labels
            ('Book', 'Chapter', 'Verse', 'Text', 'Type', 'Marker')
            followed by records.
    """
    for idx, record in enumerate(records):
        # Convert column labels to lowercase
        if idx == 0:
            cols = [col.lower() for col in record]
            records[0] = cols
        
        # Some content (headings, verses) contain trailing spaces or newlines
        # Remove the trailing whitespace from every record's text
        else:
            records[idx][3] = record[3].rstrip()


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
source_directory = os.path.join(base_dir, 'sources')
gen_usfm = os.path.join(source_directory, 'bsb_usfm/01GENBSB.SFM')
input_usfm_str = open(gen_usfm,"r", encoding='utf8').read()

my_parser = USFMParser(input_usfm_str)

# errors = my_parser.errors
# print(errors)

# TODO: Extract books and their abbreviations

# This outputs a list of lists (column labels followed by markup records)
# 'Book', 'Chapter', 'Verse', 'Text', 'Type', 'Marker'
markup_records = my_parser.to_list() 
format_records(markup_records)

verses = my_parser.to_list(None, Filter.TEXT)
format_records(verses)

# TODO: Save list output to SQLite markup table

with open(os.path.join(base_dir, 'databases/gen_markup.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(markup_records)

with open(os.path.join(base_dir, 'databases/gen_verses.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(verses)
