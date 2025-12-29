"""Schema and functions based schema on
https://github.com/JStadnik619/bible_databases/blob/master/scripts/export_sqlite_database.py
"""

import os
import sqlite3


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
        for chapter in book['chapters']:
            for verse in chapter['verses']:
                cursor.execute("""
                INSERT INTO verses (book_id, chapter, verse, text)
                VALUES (?, ?, ?, ?);
                """, (book_index, chapter['chapter'], verse['verse'], verse['text']))

# TODO: Migrate these methods from berea
# create_abbreviations_table
# create_resource_tables
# create_fts_verses_table
# create_bible_db