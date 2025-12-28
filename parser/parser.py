def read_usfm(filepath):
    with open(filepath, 'r') as file:
        usfm = file.read()
        # breakpoint()
        print(usfm)


# TODO: Might need to use a generator, since some books are 3k+ lines
def parse_usfm(book):
    """_summary_

    Args:
        book (str): the content of a book's USFM file.
    """
    verses = []
    
    for idx, line in enumerate(book.split('\n')):
        if line.contains('\v'):
            verse = {}
            # Get verse number
            # Get verse text

        # TODO: Append blank line tags
        # TODO: Prepend list item tags

        # TODO: Ignore the rest of the markup

