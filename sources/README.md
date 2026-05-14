# Translation Parsing Errors
## LEB
- Need to skip front matter (`00 ENG[B]LEB2012.sfm`)
- Need to convert `/sdo` to `/sd` to parse without crashing
- The parser doesn't like when multiple `/xt` are in the same row (eg. Matt ln. 15)