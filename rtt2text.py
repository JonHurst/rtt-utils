#!/usr/bin/python3

#usage: rtt2text.py rtt_file

import sys
import os
import xml.etree.ElementTree as et
import xml.etree.ElementInclude as ei
import re
import argparse


def tags(p, t):
    retval = set()
    tags = p.find("tags[@class='%s']" % t)
    if tags == None: return retval
    for tag in tags.findall("tag"):
        retval.add(tag.text)
    return retval


def process_heading(out_lines, heading_regexp, heading_blocks):
    #find the line containing the heading
    if heading_regexp == "":
        hdg = re.compile(r"\w+")
    else:
        hdg = re.compile(heading_regexp)
    prev_blank, next_blank, hdg_line = -1, -1, -1
    for c, l in enumerate(out_lines):
        if l == "":
            prev_blank = c
        elif hdg.search(l):
            hdg_line = c
            break
    if hdg_line == -1: return
    if heading_blocks > 1: multi_block_heading = True
    while heading_blocks:
        c += 1
        if out_lines[c] != "":
            continue
        if heading_blocks == 1:
            out_lines[c] = "::blank 2::"
        heading_blocks -= 1
    open_str = "::blank 4::"
    if prev_blank == -1:
        out_lines.insert(0, open_str)
    else:
        out_lines[prev_blank] = open_str


def process_page(p, open_mf, close_mf, heading_regexp="", heading_blocks=1):
    out_lines = []
    #process easy inline formatting
    ot, ct = open_mf, close_mf
    inline_tags = tags(p, "inline_formatting")
    if len(inline_tags) == 1:
        if "italics" in inline_tags:
            ot, ct = "_", "_"
        elif "smallcaps" in inline_tags:
            ot, ct = "", ""
    for l in p.find("text").text.splitlines():
        l = l.rstrip()
        l = re.sub(r" ?– ?", "--", l)
        l = re.sub(r"—+", "----", l)
        l = l.replace(open_mf, ot).replace(close_mf, ct)
        out_lines.append(l)
    out_lines.append("::page %s::" % p.attrib["id"])
    if "heading" in tags(p, "block_formatting"):
        process_heading(out_lines, heading_regexp, heading_blocks)
    return "\n".join(out_lines)


def main():
    parser = argparse.ArgumentParser(description='Create text with wrapping directives from rtt.')
    parser.add_argument("rtt_file", help="RTT file.")
    parser.add_argument("-r", "--heading_regexp", default="", help="Regexp to identify a chapter heading")
    parser.add_argument("-b", "--heading_blocks", type=int, choices=[1, 2],
                        default=1, help="The number of blocks in a chapter heading.")
    args = parser.parse_args()
    rtt_file = os.path.abspath(args.rtt_file)
    if not os.path.isfile(rtt_file):
        print(rtt_file, "is not a file\n", file="stderr")
        parser.print_help()
        sys.exit(-1)
    rtt = et.parse(rtt_file)
    pages = rtt.find("pages")
    os.chdir(os.path.dirname(rtt_file))
    ei.include(pages)
    open_mf = pages.attrib["microformatting-open"]
    close_mf = pages.attrib["microformatting-close"]
    pages_text = []
    first_page_text = pages.find("page/text")
    if first_page_text.text[0] != "\n":
        first_page_text.text = "\n" + first_page_text.text
    for p in pages.findall("page"):
        pages_text.append(process_page(p, open_mf, close_mf,
                                       args.heading_regexp, args.heading_blocks))
    sys.stdout.write("\n".join(pages_text))




if __name__ == "__main__":
    main()
