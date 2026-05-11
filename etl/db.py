"""Schema and functions based on
https://github.com/JStadnik619/bible_databases/blob/master/scripts/export_sqlite_database.py
"""

import csv
import os
import sqlite3
import json

from etl.markup import parse_usfm
from etl.utils import SOURCES_DIR, DBS_DIR


# TODO: Copy csv from berea
def import_resource_books(resource='step_bible'):
    books = []
    
    with open(f'{SOURCES_DIR}/{resource}_books.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            books.append(row['abbreviation'])
    
    return books


class BibleGenerator:
    def __init__(self, translation):
        self.translation = translation
        self.database = f"{DBS_DIR}/{self.translation}.db"
    
    def create_sqlite_db(self):
        # Create the database file if it doesn't exist
        os.makedirs(os.path.dirname(self.database), exist_ok=True)
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        return conn, cursor
    
    # TODO: Close out the conn when it's released
    def get_bible_cursor(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        # TODO: Use context manager?
        return conn.cursor()

    # TODO: Separate methods for books, verses, markup tables
    def create_translation_tables(self, data, language, cursor):
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
        """, (self.translation, translation_name, license_info))

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

        # TODO: Omit this table and make fts_verses table from query against markup?
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
    
    def create_markup_table(self, data):
        cursor = self.get_bible_cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS markup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            chapter INTEGER,
            verse INTEGER,
            text TEXT,
            type TEXT,
            marker TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
        """)
        
        # TODO: Make this a method?
        # Create a conn to commit inserts and close 
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        # TODO: Excecute many instead of inserting records one at a time?
        # TODO: Bind values using placeholders?
        for book_index, book in enumerate(data['books'], start=1):
            # Skip column labels ('book', 'chapter', 'verse', 'text', 'type', 'marker')
            for markup_record in book['markup'][1:]:
                cursor.execute("""
                INSERT INTO markup (book_id, chapter, verse, text, type, marker)
                VALUES (?, ?, ?, ?, ?, ?);
                """, (book_index, markup_record[1], markup_record[2], markup_record[3], markup_record[4], markup_record[5]))
        
        conn.commit()
        conn.close()
    
    # TODO: Copy json file from berea
    # TODO: Book names will need to correspond to a translation's USFM unless standardized
    def create_abbreviations_table(self):
        cursor = self.get_bible_cursor()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            abbreviation TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
        """)
        
        books_to_abbreviations = {}
        
        with open(f'{SOURCES_DIR}/book_abbreviations.json') as file:
            books_to_abbreviations = dict(json.load(file))
    
        # Create a conn to commit inserts and close 
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        for book, abbreviations in books_to_abbreviations.items():
            for abbreviation in abbreviations:
                params = {
                    'abbreviation': abbreviation,
                    'book': book,
                }
                
                cursor.execute(f"""
                INSERT INTO abbreviations (abbreviation, book_id)
                SELECT :abbreviation, books.id
                FROM books
                WHERE books.name = :book;
                """, params)
        
        conn.commit()
        conn.close()
    
    # TODO: Add berea-web once it renders markup
    def create_resource_tables(self):
        cursor = self.get_bible_cursor()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
        """)
        
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS resources_abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER,
            abbreviation_id INTEGER
        );
        """)
        
        # Create a conn to commit inserts and close 
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        # TODO: Insert STEP Bible dynamically
        resource='STEP Bible'
        cursor.execute(f"""
        INSERT INTO resources (name) VALUES (
            'STEP Bible'
        );
        """)
        
        conn.commit()
        conn.close()
        
        abbreviations = import_resource_books()
        
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        for abbreviation in abbreviations:
            params = {
                'abbreviation': abbreviation.lower(),
            }
            
            # TODO: Select STEP Bible id dynamically
            cursor.execute(f"""
            INSERT INTO resources_abbreviations (resource_id, abbreviation_id)
            SELECT 1, abbreviations.id
            FROM abbreviations
            WHERE abbreviations.abbreviation = :abbreviation;
            """, params)
        
        conn.commit()
        conn.close()
    
    # TODO: Create fts_verses from markup
    # 1. Create the FTS5 table
    # 2. Populate it from a SELECT verses query on markup
    def create_fts_verses_table(self):
        cursor = self.get_bible_cursor()
        cursor.execute("""
        CREATE VIRTUAL TABLE fts_verses
            USING fts5(book_id, chapter, verse, text);
        """)

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO fts_verses (book_id, chapter, verse, text)
        SELECT book_id, chapter, verse, text FROM verses;
        """)
        conn.commit()
        conn.close()
    
    def generate(self, usfm_data, language):
        # TODO: Delete preexisting database
        # TODO: Interact with connection consistently
        conn, cursor = self.create_sqlite_db()
        self.create_translation_tables(
            usfm_data,
            language,
            cursor
        )
        conn.commit()
        conn.close()
        
        self.create_markup_table(usfm_data)
        self.create_abbreviations_table()
        self.create_resource_tables()
        self.create_fts_verses_table()
        print(f"{self.translation} translation database built successfully!")


# TODO: Once this works (including markup), compare db size to berea
def main():
    # TODO: Do one translation at a time or all available?
    # TODO: Get translation info from translations.csv
    translation = 'BSB'
    usfm_data = parse_usfm(os.path.join(SOURCES_DIR, translation))
    
    bible = BibleGenerator(translation)
    # TODO: Get language from translation README
    bible.generate(usfm_data, 'ENG')


if __name__ == "__main__":
    main()
