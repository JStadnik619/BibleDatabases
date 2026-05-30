import re
from collections import defaultdict
import os


# Sets don't maintain order of verses but provide O(1) lookups
def parse_paragraph_breaks(text: str) -> dict[str, dict[int, set[int]]]:
    result = defaultdict(lambda: defaultdict(set))

    current_book = None
    current_chapter = None
    current_verse = None

    verse_pattern = re.compile(r'^\S+(?:\s+\S+)?\s+(\d+):(\d+)\t')
    divider_pattern = re.compile(r'^[-_]{10,}$')

    lines = text.splitlines()

    def find_next_reference(start_index: int):
        """
        Finds the next verse reference AND its book/chapter context.
        Used to determine if a blank-line break is valid.
        """
        next_book = current_book
        next_chapter = None

        k = start_index + 1

        while k < len(lines):
            line = lines[k].strip()

            # Detect book heading
            if divider_pattern.match(line):
                j = k + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1

                if (
                    j < len(lines)
                    and j + 1 < len(lines)
                    and divider_pattern.match(lines[j + 1].strip())
                ):
                    next_book = lines[j].strip().title()
                    k = j + 1
                    continue

            match = verse_pattern.match(lines[k])
            if match:
                next_chapter = int(match.group(1))
                break

            k += 1

        return next_book, next_chapter

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect book headings
        if divider_pattern.match(stripped):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if (
                j < len(lines)
                and j + 1 < len(lines)
                and divider_pattern.match(lines[j + 1].strip())
            ):
                current_book = lines[j].strip().title()
            continue

        # Blank line => potential paragraph break
        if not stripped:
            if (
                current_book is not None
                and current_chapter is not None
                and current_verse is not None
            ):
                next_book, next_chapter = find_next_reference(i)

                # Only keep break if still same book + chapter
                if (
                    next_book == current_book
                    and next_chapter == current_chapter
                ):
                    result[current_book][current_chapter].add(current_verse)

            continue

        # Verse line
        match = verse_pattern.match(line)
        if match:
            current_chapter = int(match.group(1))
            current_verse = int(match.group(2))

    return {
        book: dict(chapters)
        for book, chapters in result.items()
    }


def insert_b_markers(
    usfm: str,
    paragraph_breaks: dict[str, dict[int, set[int]]]
) -> str:
    lines = usfm.splitlines()
    output = []

    # Determine the book name from the \h marker
    book_name = None
    for line in lines:
        if line.startswith(r"\h "):
            book_name = line[3:].strip()
            break

    if book_name not in paragraph_breaks:
        return usfm

    breaks = paragraph_breaks[book_name]

    current_chapter = None

    chapter_pattern = re.compile(r'^\\c\s+(\d+)$')
    verse_pattern = re.compile(r'^\\v\s+(\d+)\b')

    for line in lines:
        output.append(line)

        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            current_chapter = int(chapter_match.group(1))
            continue

        verse_match = verse_pattern.match(line)
        if verse_match and current_chapter is not None:
            verse = int(verse_match.group(1))

            if verse in breaks.get(current_chapter, set()):
                output.append(r'\b')

    return '\n'.join(output)


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    
    with open(f'{path}/LEB.txt') as text_file:
        text = text_file.read()
        paragraph_breaks = parse_paragraph_breaks(text)
    
        sfm_books = sorted([f for f in os.listdir(path) if f.lower().endswith('sfm')])
        
        for sfm_book in sfm_books:
            sfm_path = f'{path}/{sfm_book}'
            with open(sfm_path, 'r', encoding='utf8') as usfm_file:
                usfm = usfm_file.read()
                
            usfm_with_paragraph_breaks = insert_b_markers(usfm, paragraph_breaks)
            
            with open(sfm_path, 'w', encoding='utf8') as usfm_file:
                usfm_file.write(usfm_with_paragraph_breaks)
    
    print("LEB USFM files updated.")
