SELECT verse, text, marker FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('q1', 'q2')
AND books.name = 'Proverbs';

SELECT verse, text, marker FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
AND books.name = 'Genesis'
AND chapter = 2
AND verse BETWEEN 10 AND 15;

SELECT verse, text, marker, type FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
AND books.name = 'Genesis'
AND chapter = 1
AND verse BETWEEN 3 AND 5;

SELECT books.name, verse, text, marker, type FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
AND books.name = 'Psalms'
AND chapter = 117
AND verse BETWEEN 1 AND 2;

-- Shorter Psalms: 117, 134, 131, 133, 15, 23
SELECT books.name, verse, text, marker, type FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
AND books.name = 'Psalms'
AND chapter = 134;

SELECT books.name, verse, text, marker, type FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
AND books.name = 'Proverbs'
AND chapter = 1
AND verse BETWEEN 1 AND 7;

SELECT verse, text, marker, type FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
AND books.name = 'Genesis'
AND chapter = 1
AND verse = 31;

-- SELECT verses from markup table
SELECT
    book_id,
    chapter,
    verse,
    GROUP_CONCAT(text, ' ') AS text
FROM markup
WHERE marker IN ('m', 'pmo', 'li1', 'q1', 'q2')
AND book_id = 1 AND chapter = 1
GROUP BY verse;

-- Do this for . , ! ? ; : ... ] )
SELECT books.name, chapter, verse, text, marker, type FROM markup
JOIN books ON markup.book_id = books.id
WHERE marker IN ('m', 'pmo', 'li1', 'q1', 'q2')
AND text LIKE '%!';