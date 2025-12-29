def read_usfm(filepath):
    with open(filepath, 'r') as file:
        usfm = file.read()
        # breakpoint()
        print(usfm)


def set_or_append_text(verse, text):
    if verse.get('text'):
        verse['text'] += ' ' + text
    else:
        verse['text'] = text


# TODO: Might need to use a generator, since some books are 3k+ lines
def parse_usfm(book):
    """_summary_

    Args:
        book (str): the content of a book's USFM file.
    """
    verses = []
    verse = {}
    next_verse_prefix = ''
    
    for line in book.split('\n'):
        # breakpoint()
        if line.startswith('\v'):
            if verse:
                verses.append(verse)
                verse = {}

            # Verse format: \v <verse number> <verse text> 
            line_split = line.split(' ', 2)
            verse['verse'] = int(line_split[1])

            if next_verse_prefix:
                verse['text'] = next_verse_prefix
                next_verse_prefix = ''
            
            set_or_append_text(verse, line_split[2].rstrip())
        elif line == '\li1 ':
            next_verse_prefix = line.rstrip()
        elif line.startswith('\li'):
            set_or_append_text(verse, line.rstrip())
        elif line.startswith('\b'):
            set_or_append_text(verse, line)
            
        # Ignore all other markup
        else:
            continue

    # Add last verse
    verses.append(verse)
    
    return verses
