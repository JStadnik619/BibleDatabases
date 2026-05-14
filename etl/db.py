"""Schema and functions based on
https://github.com/JStadnik619/bible_databases/blob/master/scripts/export_sqlite_database.py
"""

import csv
import os
import sqlite3
import json
import sys

from etl.markup import parse_usfm
from etl.utils import SOURCES_DIR, DBS_DIR


def import_resource_books(resource='step_bible'):
    books = []
    
    with open(f'{SOURCES_DIR}/{resource}_books.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            books.append(row['abbreviation'])
    
    return books


def import_translations_data(translation=None):
    """
    Returns specified translation data if provided, otherwise returns data for
    all translations.
    """
    translations = []
    
    with open(f'{SOURCES_DIR}/translations.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if translation:
                if row['translation'] == translation:
                    translations.append(row)
            else:
                translations.append(row)
            
    return translations


class BibleGenerator:
    def __init__(self, translation, title, license, source):
        self.translation = translation
        self.title = title
        self.license = license
        self.source = source
        self.database = f"{DBS_DIR}/{self.translation}.db"
    
    def delete_sqlite_db(self):
        if os.path.exists(self.database):
            os.remove(self.database)
    
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
    def create_translation_tables(self, data, cursor):
        """
        _summary_

        Args:
            data (dict): books and verses parsed from the USFM file.
        """

        # Create translations table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            translation TEXT PRIMARY KEY,
            title TEXT,
            license TEXT,
            source TEXT
        );
        """)
        cursor.execute("""
        INSERT OR IGNORE INTO translations (translation, title, license, source)
        VALUES (?, ?, ?, ?);
        """, (self.translation, self.title, self.license, self.source))

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
        SELECT
            book_id,
            chapter,
            verse,
        TRIM(GROUP_CONCAT(TRIM(text), ' ')) AS text
        FROM markup
        WHERE marker IN ('m', 'pmo', 'p', 'pc', 'sc', 'add', 'li1', 'li2', 'q1', 'q2')
        GROUP BY book_id, chapter, verse;
        """)
        conn.commit()
        conn.close()
    
    def generate(self, usfm_data, language):
        self.delete_sqlite_db()
        # TODO: Interact with connection consistently
        conn, cursor = self.create_sqlite_db()
        self.create_translation_tables(
            usfm_data,
            cursor
        )
        conn.commit()
        conn.close()
        
        self.create_markup_table(usfm_data)
        self.create_abbreviations_table()
        self.create_resource_tables()
        self.create_fts_verses_table()
        print(f"{self.translation} translation database built successfully!")


def main(args):
    translations = []
    
    # Generate all translations by default
    if len(args) < 1:
        translations = import_translations_data()
    elif len(args) == 1:
        translations = import_translations_data(args[0])
    else:
        print("Usage: python -m etl.db <translation>")
        return
    
    for translation in translations:
        usfm_data = parse_usfm(os.path.join(SOURCES_DIR, translation['translation']))
        bible = BibleGenerator(**translation)
        # TODO: Get language from translation translations.csv
        bible.generate(usfm_data, 'ENG')


if __name__ == "__main__":
    main(sys.argv[1:])
