<!-- TODO: Rename repo to BibleDatabases -->
# Bible Translations with Formatting, Cross References, and FTS
This is a collection of SQLite databases containing the markup records from
each translation's [USFM](https://paratext.org/usfm/) file. Records include 
verse text, formatting (eg. paragraph breaks, list or poetry indentation),
headings, footnotes, and cross references.

The databases also feature
[full-text search](https://en.wikipedia.org/wiki/Full-text_search) for verses.

## Available Translations
- **BSB (en)**: Berean Standard Bible
- **KJV (en)**: KJV Cambridge Paragraph Bible
- **LEB (en)**: The Lexham English Bible

## Database Schema
#### Table: `books`
This table lists all the books in the given translation of the Bible.

| Column Name | Type | Nullable | Key         | Default | Extra          | Description                      |
| ----------- | ---- | -------- | ----------- | ------- | -------------- | -------------------------------- |
| `id`        | int  | NO       | Primary Key | NULL    | auto_increment | Unique identifier for each book. |
| `name`      | text | YES      |             | NULL    |                | The name of the book.            |

#### Table: `markup`
This table contains all the markup records in the given translation of the Bible.

| Column Name | Type | Nullable | Key         | Default | Extra          | Description                                         |
| ----------- | ---- | -------- | ----------- | ------- | -------------- | --------------------------------------------------- |
| `id`        | int  | NO       | Primary Key | NULL    | auto_increment | Unique identifier for each markup record.           |
| `name`      | text | YES      |             | NULL    |                | The name of the book.                               |
| `book_id`   | int  | YES      |             | NULL    |                | The ID of the book (foreign key to `books`).        |
| `chapter`   | int  | YES      |             | NULL    |                | The chapter number.                                 |
| `verse`     | int  | YES      |             | NULL    |                | The verse number.                                   |
| `text`      | text | YES      |             | NULL    |                | The text of the record.                             |
| `type`      | text | YES      |             | NULL    |                | The kind/category corresponding to the USFM marker. |
| `marker`    | text | YES      |             | NULL    |                | The USFM marker of the record.                      |

#### Table: `abbreviations`
This table maps abbreviations to the books in the given translation of the Bible.

| Column Name    | Type | Nullable | Key         | Default | Extra          | Description                                  |
| -------------- | ---- | -------- | ----------- | ------- | -------------- | -------------------------------------------- |
| `id`           | int  | NO       | Primary Key | NULL    | auto_increment | Unique identifier for each markup record.    |
| `book_id`      | int  | YES      |             | NULL    |                | The ID of the book (foreign key to `books`). |
| `abbreviation` | text | YES      |             | NULL    |                | The abbreviation of the book.                |

#### Table: `fts_verses`
This table contains all the verses in the given translation of the Bible,
created with the [SQLite FTS5 Extension](https://www.sqlite.org/fts5.html)
to enable full-text search.

| Column Name | Type | Nullable | Key | Default | Extra | Description                                  |
| ----------- | ---- | -------- | --- | ------- | ----- | -------------------------------------------- |
| `book_id`   | int  | YES      |     | NULL    |       | The ID of the book (foreign key to `books`). |
| `chapter`   | int  | YES      |     | NULL    |       | The chapter number.                          |
| `verse`     | int  | YES      |     | NULL    |       | The verse number.                            |
| `text`      | text | YES      |     | NULL    |       | The text of the verse.                       |

#### Table: `translations`
This table contains information about the available Bible translations.

| Column Name   | Type | Nullable | Key         | Default | Extra | Description                                   |
| ------------- | ---- | -------- | ----------- | ------- | ----- | --------------------------------------------- |
| `translation` | text | NO       | Primary Key | NULL    |       | The abbreviation of the translation.          |
| `title`       | text | YES      |             | NULL    |       | The full title of the translation.            |
| `license`     | text | YES      |             | NULL    |       | The license information for the translation.  |
| `source`      | text | YES      |             | NULL    |       | The direct download link for the translation. |

# Related Projects
- [berea](https://github.com/JStadnik619/berea):
  Python client and command-line tool for referencing and searching passages
- [berea-web](https://github.com/JStadnik619/berea-web):
  Flask web app for full-text searching Scripture