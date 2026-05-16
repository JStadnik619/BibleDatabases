# Procedure For Adding Translations
1. Add a direct link to the translation's USFM to `translations.csv`
2. Parse the USFM into SQLite
3. Determine text markers used by translation, eg.
```sql
SELECT DISTINCT(marker) FROM markup
WHERE type IN ('para', 'char')
AND verse != ''
ORDER BY marker ASC;
```
4. Update downstream queries (eg. for building `fts_verses`) and rendering algorithm if necessary
5. Compare verse contents against [scrollmapper databases](https://github.com/JStadnik619/bible_databases)
  - Export a table to a file:
```
sqlite3 -header databases/BSB.db "SELECT book_id, chapter, verse FROM fts_verses;" > "bsb_fts_verses_new.txt"
```
  - Diff the two files

# Translation Notes
## BSB
- [bible_databases](https://github.com/JStadnik619/bible_databases) and eBible.org use the 2nd edition of the BSB, whereas the 3rd edition is used here
### Parsing Errors
- There's an empty `\d` at Zechariah 12:1, which should be `\m` instead
```
[('At Point(row=541, column=0)', '\\d\n\\v 1 This is the burden of the word of the LORD concerning Israel.'), ('At Point(row=542, column=65)', '.')]
```
## KJV
- Using [KJV Cambridge Paragraph Bible](https://ebible.org/Scriptures/details.php?id=engkjvcpb)
  since the [King James (Authorized) Version](https://ebible.org/Scriptures/details.php?id=eng-kjv2006)
  contains Strong's numbers
## LEB
### Parsing Errors
- Need to skip front matter (`00 ENG[B]LEB2012.sfm`)
- Need to convert `/sdo` to `/sd` to parse without crashing
- The parser doesn't like when multiple `/xt` are in the same row (eg. Matt ln. 15)