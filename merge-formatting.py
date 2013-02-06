#!/usr/bin/python3

import sys
import os
import re
import xml.etree.ElementTree as et

def extract_tags(filename):
    page_break = re.compile(r"-----File: (\d+)")
    block_dict = {"nowrap_block": "/*",
                  "wrap_block": "/#",
                  "thought_break": "<tb",
                  "illustration": "[Illustration",
                  "footnote": "[Footnote",
                  "sidenote": "[Sidenote",
                  "blank_page": "[Blank Page]"}
    inline_dict = {"italics": "<i>",
                   "smallcaps": "<sc>",
                   "bold": "<b>",
                   "gesperrt": "<g>",
                   "misc_inline": "<f>",
                   "superscript": "^{",
                   "subscript": "_{"}
    current_page = ""
    blank_count = 0
    block_tags = {}
    inline_tags = {}
    for l in open(filename, encoding="latin-1"):
        mo = page_break.match(l)
        if mo:
            current_page = mo.group(1)
            block_tags[current_page] = set()
            inline_tags[current_page] = set()
            blank_count = 0
            continue
        l = l.strip()
        if l == "":
            blank_count += 1
            if blank_count == 4:
                block_tags[current_page].add("heading")
        else:
            blank_count = 0
        for k in block_dict:
            if l.find(block_dict[k]) != -1:
                block_tags[current_page].add(k)
        for k in inline_dict:
            if l.find(inline_dict[k]) != -1:
                inline_tags[current_page].add(k)
    return (block_tags, inline_tags)


def set_tags(p, block_tags, inline_tags):
    for (cls, tags) in (("block_formatting", block_tags),
                        ("inline_formatting", inline_tags)):
        if tags:
            tags_elem = p.find("tags[@class='" + cls + "']")
            if not tags_elem:
                tags_elem = et.SubElement(p, "tags", {"class": cls})
            for t in tags:
                tag = et.SubElement(tags_elem, "tag")
                tag.text = t


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem) and elem.tag != "text":
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main():
    if (len(sys.argv) != 3 or
        not os.path.isfile(sys.argv[1]) or
        not os.path.isfile(sys.argv[2])):
        print("Usage: ", sys.argv[0], "f2_file rtt_file")
        sys.exit(-1)
    block_tags, inline_tags = extract_tags(sys.argv[1])
    et.register_namespace("xi", "http://www.w3.org/2001/XInclude")
    rtt = et.ElementTree(file=sys.argv[2])
    for p in rtt.findall(".//page"):
        pn = p.attrib["id"]
        set_tags(p, block_tags[pn], inline_tags[pn])
    indent(rtt.getroot())
    rtt.write(sys.stdout, encoding="unicode", xml_declaration=True)

if __name__ == "__main__":
    main()
