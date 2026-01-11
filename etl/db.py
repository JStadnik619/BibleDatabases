"""Schema and functions based on
https://github.com/JStadnik619/bible_databases/blob/master/scripts/export_sqlite_database.py
"""

import os
import sqlite3

from etl.markup import parse_usfm


def create_sqlite_db(db_path):
    # Create the database file if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def generate_translation_tables(data, language, translation, cursor):
    """
    _summary_

    Args:
        data (dict): books and verses parsed from the USFM file.
    """
    # json_path = os.path.join(source_directory, language, translation, f"{translation}.json")
    # with open(json_path, 'r', encoding='utf-8') as file:
    #     data = json.load(file)

    # TODO: Get license info from the source page
    # readme_path = os.path.join(source_directory, language, translation, "README.md")
    # with open(readme_path, 'r', encoding='utf-8') as file:
    #     translation_name = file.readline().strip()
    #     license_info = "Unknown"
    #     for line in file:
    #         if line.startswith("**License:**"):
    #             license_info = line.split("**License:** ")[1].strip()
    license_info = "None"
    # TODO: Read name from Settings.xml FullName
    translation_name = "Berean Standard Bible"

    # Create translations table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS translations (
        translation TEXT PRIMARY KEY,
        title TEXT,
        license TEXT
    );
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO translations (translation, title, license)
    VALUES (?, ?, ?);
    """, (translation, translation_name, license_info))

    # Create books table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
    """)

    # Insert books
    for book in data['books']:
        cursor.execute("INSERT INTO books (name) VALUES (?);", (book['name'],))

    # Create verses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        chapter INTEGER,
        verse INTEGER,
        text TEXT,
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    """)

    # Insert verses
    for book_index, book in enumerate(data['books'], start=1):
        # Skip column labels ('book', 'chapter', 'verse', 'text', 'type', 'marker')
        for verse in book['verses'][1:]:
            cursor.execute("""
            INSERT INTO verses (book_id, chapter, verse, text)
            VALUES (?, ?, ?, ?);
            """, (book_index, verse[1], verse[2], verse[3]))
    
    # TODO: Insert markup

# TODO: Migrate these methods from berea
# create_abbreviations_table
# create_resource_tables
# create_fts_verses_table
# create_bible_db

def main():
    # Set base directories relative to the script location
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    source_directory = os.path.join(base_dir, 'sources')

    # TODO: Do one translation at a time or all available?
    usfm_data = parse_usfm(os.path.join(source_directory, 'bsb_usfm'))

    translation = usfm_data['translation']
    target_db_path = os.path.join(base_dir, f"databases/{translation}.db")

    conn, cursor = create_sqlite_db(target_db_path)
    language = 'ENG'
    generate_translation_tables(
        usfm_data,
        language,
        translation,
        cursor
    )

    conn.commit()
    conn.close()

    print(f"{translation} translation database built successfully!")


if __name__ == "__main__":
    main()
