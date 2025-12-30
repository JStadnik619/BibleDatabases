import pytest

from etl.parser import parse_verses


@pytest.mark.parametrize(
    "passage, verses",
    [
        (
            # Gen 2:10-15
            (
                "\v 10 Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters: \n"
                "\b\n"
                "\li1 \n"
                "\v 11 The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold. \n"
                "\v 12 And the gold of that land is pure, and bdellium and onyx are found there. \n"
                "\b\n"
                "\li1 \n"
                "\v 13 The name of the second river is the Gihon; it winds through the whole land of Cush. \n"
                "\b\n"
                "\li1 \n"
                "\v 14 The name of the third river is the Tigris; it runs along the east side of Assyria. \n"
                "\b\n"
                "\li1 And the fourth river is the Euphrates. \n"
                "\b\n"
                "\m \n"
                "\v 15 Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.\n" 
                "\b\n"
                "\m \n"
            ),
            [
                {
                    'book': '',
                    'chapter': 0,
                    'verse': 10,
                    # Blank lines are appended to verses
                    'text': "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters: \b",
                    'raw_text': "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters:",
                },
                {
                    'book': '',
                    'chapter': 0,
                    'verse': 11,
                    # List items are prepended to verses
                    'text': "\li1 The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold.",
                    'raw_text': "The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold.",
                },
                {
                    'book': '',
                    'chapter': 0,
                    'verse': 12,
                    'text': "And the gold of that land is pure, and bdellium and onyx are found there. \b",
                    'raw_text': "And the gold of that land is pure, and bdellium and onyx are found there.",
                },
                {
                    'book': '',
                    'chapter': 0,
                    'verse': 13,
                    'text': "\li1 The name of the second river is the Gihon; it winds through the whole land of Cush. \b",
                    'raw_text': "The name of the second river is the Gihon; it winds through the whole land of Cush.",
                },
                {
                    'book': '',
                    'chapter': 0,
                    'verse': 14,
                    'text': "\li1 The name of the third river is the Tigris; it runs along the east side of Assyria. \b \li1 And the fourth river is the Euphrates. \b",
                    'raw_text': "The name of the third river is the Tigris; it runs along the east side of Assyria. And the fourth river is the Euphrates.",
                },
                {
                    'book': '',
                    'chapter': 0,
                    'verse': 15,
                    'text': "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it. \b",
                    'raw_text': "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.",
                },
            ],
        ),
    ]
)
def test_parse_verses(passage, verses):
    assert parse_verses(passage) == verses