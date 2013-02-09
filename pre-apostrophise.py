#!/usr/bin/python3

import sys
import re

def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "apostrophe_file")
        sys.exit(-1)
    text = sys.stdin.read()
    apos_list = open(sys.argv[1], encoding="utf-8").read().splitlines()
    for a in apos_list:
        a = a.strip()
        r = a.replace("'", '\u02bc')
        text = re.sub(r"(\W|^)%s(\W|$)" % a, r"\1%s\2" % r, text, flags=re.MULTILINE)
    print(text)


if __name__ == "__main__":
    main()
