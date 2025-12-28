import pytest

from parser.parser import parse_usfm


@pytest.mark.parametrize(
    "passage, verses",
    [
        (
            (
                "\v 10 Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters: "
                "\b"
                "\li1 "
                "\v 11 The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold. "
                "\v 12 And the gold of that land is pure, and bdellium and onyx are found there. "
                "\b"
                "\li1 "
                "\v 13 The name of the second river is the Gihon; it winds through the whole land of Cush. "
                "\b"
                "\li1 "
                "\v 14 The name of the third river is the Tigris; it runs along the east side of Assyria. "
                "\b"
                "\li1 And the fourth river is the Euphrates. "
                "\b"
                "\m "
                "\v 15 Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it." 
                "\b"
                "\m "
            ),
            [
                {
                    'verse': 10,
                    # Blank lines would have to be appended to verses
                    'text': "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters:\b",
                },
                {
                    'verse': 11,
                    # List items would have to be prepended to verses
                    'text': "\li1The name of the first river is Pishon; it winds through the whole land of Havilah, where there is gold.",
                },
                {
                    'verse': 12,
                    'text': "And the gold of that land is pure, and bdellium and onyx are found there.\b",
                },
                {
                    'verse': 13,
                    'text': "\li1The name of the second river is Gihon; it winds through the whole land of Cush.\b",
                },
                {
                    'verse': 14,
                    'text': "\li1The name of the third river is Tigris; it runs along the east side of Assyria.\b\li1And the fourth river is the Euphrates.\b",
                },
                {
                    'verse': 15,
                    'text': "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.\b",
                },
            ],
        ),
    ]
)
def test_parse_usfm(passage, verses):
    assert parse_usfm(passage) == verses