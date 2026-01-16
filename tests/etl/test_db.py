import pytest

from etl.db import BibleGenerator


def test_create_markup_table():
    data = {
        'books': [
            {
                'name': 'Genesis',
                'markup': [
                    ['book', 'chapter', 'verse', 'text', 'type', 'marker']
                    ["GEN", 2, 10, "", "verse", "v"],
                    ["GEN", 2, 10, "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters:\n", "para", "m"],
                    ["GEN", 2, 10, "", "para", "b"],

                    ["GEN", 2, 11, "", "verse", "v"],
                    ["GEN", 2, 11, "The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold.\n", "para", "li1"],

                    ["GEN", 2, 12, "", "verse", "v"],
                    ["GEN", 2, 12, "And the gold of that land is pure, and bdellium and onyx are found there.\n", "para", "li1"],
                    ["GEN", 2, 12, "", "para", "b"],

                    ["GEN", 2, 13, "", "verse", "v"],
                    ["GEN", 2, 13, "The name of the second river is the Gihon; it winds through the whole land of Cush.\n", "para", "li1"],
                    ["GEN", 2, 13, "", "para", "b"],

                    ["GEN", 2, 14, "", "verse", "v"],
                    ["GEN", 2, 14, "The name of the third river is the Tigris; it runs along the east side of Assyria.\n", "para", "li1"],
                    ["GEN", 2, 14, "", "para", "b"],
                    ["GEN", 2, 14, "And the fourth river is the Euphrates.\n", "para", "li1"],
                    ["GEN", 2, 14, "", "para", "b"],

                    ["GEN", 2, 15, "", "verse", "v"],
                    ["GEN", 2, 15, "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.\n", "para", "m"],
                    ["GEN", 2, 15, "", "para", "b"],
                ]
            }
        ]
    }
    
    bible = BibleGenerator('BSB-test')
    bible.create_markup_table(data)
    # TODO: Assert that markup is actually contained in the db
    # TODO: Assert that the column labels are NOT inserted as a row
    # TODO: Delete test db
