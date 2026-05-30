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
<!-- TODO: Compile sqldiff with FTS5 enabled to sqldiff fts_verses -->
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
- Update `\h Song` to `\h Song of Solomon` to enable its abbreviations
## KJV
- Using [KJV Cambridge Paragraph Bible](https://ebible.org/Scriptures/details.php?id=engkjvcpb)
  since the [King James (Authorized) Version](https://ebible.org/Scriptures/details.php?id=eng-kjv2006)
  contains Strong's numbers
## LEB
- The LEB's USFM does not contain blank lines, so paragraph breaks are parsed
  from the [plain text release](https://web.archive.org/web/20181005033818/http://lexhamenglishbible.com/download/LEB.txt)
  and inserted into the USFM files
### Parsing Errors
- Need to skip front matter (`00 ENG[B]LEB2012.sfm`)
- Need to convert `\sd0` to `\sd` to parse without raising exceptions
- `\qs` and `\qs*` raise exceptions 
- `\xt` are not closed with `\xt*`
  - This is unresolved, but probably inconsequential until implementing cross 
    reference rending
- `\m1` tags must be converted to `\m`
- `\p1` tags must be converted to `\p`
- Footnotes (`\ft`) will duplicate `\add` content when describing translator's methodology 
  - Resolved by performing the following find and replaces:
    - find: `(\\ft\s+﻿\*Here “)\\add\s+([^\\]+?)\\add\*` replace: `$1$2`
    - find: `(\\ft\s+\*Here “)\\add\s+([^\\]+?)\\add\*”` replace: `$1$2”`
- Update `\h Psalm` to `\h Psalms` to enable its abbreviations

<!-- TODO: Add script to download source USFMs from translations.csv -->
<!-- Base on [this ebible script](https://github.com/BibleNLP/ebible/blob/main/code/python/ebible.py) -->