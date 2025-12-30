import re


# TODO: Return a generator?
def read_sfm(filepath):
    print(f'Reading file {filepath}')
    with open(filepath, 'r') as file:
        sfm = file.read()
        return sfm


def set_or_append_text(verse, text):
    if verse.get('text'):
        verse['text'] += ' ' + text
    else:
        verse['text'] = text


def remove_markup(text):
    raw_text = text
    tags = [
        '\b',
        '\li1',
    ]
    for tag in tags:
        raw_text = raw_text.replace(tag, '')
    # Remove extra spaces left from removing tags
    return re.sub(r'\s+', ' ', raw_text.strip())


# TODO: Might need to use a generator, since some books are 3k+ lines
# TODO: Parse \li2
def parse_verses(sfm_content):
    """_summary_

    Args:
        sfm_content (str): the content of a book's USFM file.
    """
    verses = []
    book = ''
    chapter = 0
    verse = {}
    next_verse_prefix = ''
    
    for line in sfm_content.split('\n'):
        # breakpoint()
        if line.startswith('\h'):
            book = int(line[2:])
        elif line.startswith('\c'):
            chapter = int(line[2:])
        elif line.startswith('\v'):
            if verse:
                verse['book'] = book
                verse['chapter'] = chapter
                verse['raw_text'] = remove_markup(verse['text'])
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
    verse['book'] = book
    verse['chapter'] = chapter
    verse['raw_text'] = remove_markup(verse['text'])
    verses.append(verse)
    
    return verses


# TODO: Verses will exceed 31k, use generator?
def parse_usfm(path):
    # TODO: Read translation/license metadata from Setting.xml
    # TODO: Return a list of books and their abbreviations from BookNames.xml
    sfm_books = [f for f in os.listdir(path) if f.lower().endswith('.sfm')]
    verses = []
    for sfm_book in sfm_books:
        sfm_content = read_sfm(sfm_book)
        verses += parse_verses(sfm_content)
    return verses
