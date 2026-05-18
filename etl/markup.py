"""
POC for using usfm-grammar instead of implementing my own USFM parser.
Based on https://github.com/Bridgeconn/usfm-grammar/tree/master/py-usfm-parser
"""

# TODO: Rename this module

import os

from usfm_grammar import USFMParser


def format_records(records):
    """
    Convert column labels to lowercase and remove trailing whitespace from the
    text column.

    Args:
        records (list): a list of lists containing column labels
            ('book', 'chapter', 'verse', 'text', 'type', 'marker')
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


# BUG: BSB/38ZECBSB.SFM
# Exception: Errors present:
#         At Point(row=541, column=0):\d
# \v 1 This is the burden of the word of the LORD concerning Israel.
#         At Point(row=542, column=65):.
def extract_book_data(usfm):
    """Extract translation, book, markup, and verses from USFM file.

    Args:
        usfm (str): path to the USFM file.

    Returns:
        dict: the file's translation, book, markup, and verses.
    """
    data = {}

    with open(usfm, "r", encoding='utf8') as file:
        usfm_content = file.read()
        parser = USFMParser(usfm_content)

        errors = parser.errors
        if errors:
            print(errors)

        data['name'] = parser.to_list(include_markers=['h'], ignore_errors=True)[1][3].rstrip()
        print(f"Parsing: {data['name']}")

        # This outputs a list of lists (column labels followed by markup records)
        # 'Book', 'Chapter', 'Verse', 'Text', 'Type', 'Marker'
        markup = parser.to_list(ignore_errors=True) 
        format_records(markup)
        data['markup'] = markup
        data['abbreviation'] = markup[1][0]
    
    return data


# TODO: Commit verses and markup to db for each book?
def parse_usfm(path):
    sfm_books = sorted([f for f in os.listdir(path) if f.lower().endswith('sfm')])
    translation_data = {
        'abbreviations': [],
        'books': [],
    }
    for sfm_book in sfm_books:
        try:
            book_data = extract_book_data(f"{path}/{sfm_book}")
            translation_data['books'].append(book_data)
        except Exception as ex:
            print(f"\nError parsing {path}/{sfm_book}\n")
            raise ex

    return translation_data
