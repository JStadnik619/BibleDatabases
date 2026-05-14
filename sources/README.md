# Procedure For Adding Translations
1. Add a direct link to the translation's USFM to `translations.csv`.
2. Parse the USFM into SQLite
3. Determine text markers used by translation, eg.
```sql
SELECT DISTINCT(marker) FROM markup
WHERE type IN ('para', 'char')
AND verse != ''
ORDER BY marker ASC;
```
4. Update downstream queries (eg. for building `fts_verses`) and rendering algorithm if necessary.

# Translation Parsing Errors
## LEB
- Need to skip front matter (`00 ENG[B]LEB2012.sfm`)
- Need to convert `/sdo` to `/sd` to parse without crashing
- The parser doesn't like when multiple `/xt` are in the same row (eg. Matt ln. 15)