"""
POC for using usfm-grammar instead of implementing my own USFM parser.
Based on https://github.com/Bridgeconn/usfm-grammar/tree/master/py-usfm-parser
"""

import os
import csv

from usfm_grammar import USFMParser, Filter


def format_records(records):
    """
    Convert column labels to lowercase and remove trailing whitespace from the
    text column.

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


def extract_data(usfm):
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

        # errors = parser.errors
        # print(errors)

        # TODO: Each call it parser is slow, get translation name once per translation
        # TODO: Not all translations contain the translation name in \id
        # or come with Settings.xml
        data['translation'] = parser.to_list(include_markers=['id'])[1][3][2:]
        data['book'] = parser.to_list(include_markers=['h'])[1][3].rstrip()
        print(f"Parsing {data['translation']}: {data['book']}")

        # This outputs a list of lists (column labels followed by markup records)
        # 'Book', 'Chapter', 'Verse', 'Text', 'Type', 'Marker'
        markup = parser.to_list() 
        format_records(markup)
        data['markup'] = markup
        data['abbreviation'] = markup[1][0]

        verses = parser.to_list(None, Filter.TEXT)
        format_records(verses)
        data['verses'] = verses
    
    return data


# TODO: Commit verses and markup to db for each book?
def parse_usfm(path):
    # TODO: Read translation/license metadata from Setting.xml
    # TODO: Return a list of books and their abbreviations from BookNames.xml
    sfm_books = [f for f in os.listdir(path) if f.lower().endswith('.sfm')]
    verses = []
    for sfm_book in sfm_books:
        sfm_content = read_sfm(sfm_book)
        verses += parse_verses(sfm_content)
    return verses


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    source_directory = os.path.join(base_dir, 'sources')
    gen_usfm = os.path.join(source_directory, 'bsb_usfm/01GENBSB.SFM')

    data = extract_data(gen_usfm)

    with open(os.path.join(base_dir, 'databases/gen_markup.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data['markup'])

    with open(os.path.join(base_dir, 'databases/gen_verses.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data['verses'])
