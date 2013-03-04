#!/usr/bin/python3

#usage: rtt2latex.py rtt_file

import sys
import os
import xml.etree.ElementTree as et
import xml.etree.ElementInclude as ei
import html
import re

heading_regexp = "CHAPTER|INTRODUCTION|LETTER|PREFACE"

latex_escape_table = [
    ("\\", r"\textbackslash"),
    ("%", r"\%"),
    ("–", "--"),
    ("—", "---"),
    ("$", r"\$"),
    ("{", r"\{"),
    ("_", r"\_"),
    ("&", r"\&"),
    ("#", r"\#"),
    ("}", r"\}"),
    ("~", r"\textasciitilde"),
    ("“‘", "“\,‘"),
    ("‘“", "‘\,“"),
    (": --", ":--")
    ]


def text_to_latex(text):
    #escape the special characters
    for l in latex_escape_table:
        text = text.replace(l[0], l[1])
    return text


def tags(p, t):
    retval = set()
    tags = p.find("tags[@class='%s']" % t)
    if tags == None: return retval
    for tag in tags.findall("tag"):
        retval.add(tag.text)
    return retval


def process_heading(out_lines, heading_regexp):
    #find the line containing the heading
    if heading_regexp == "":
        hdg = re.compile(r"\w+")
    else:
        hdg = re.compile(heading_regexp)
    hdg_line = -1
    for c, l in enumerate(out_lines):
        if hdg.search(l):
            hdg_line = c
            break
    if hdg_line == -1: return
    out_lines[hdg_line] = r"\Chapter{" + out_lines[hdg_line] + "}"


def process_page(p, open_mf, close_mf, heading_regexp=""):
    out_lines = []
    #process easy inline formatting
    open_mf = text_to_latex(open_mf)
    close_mf = text_to_latex(close_mf)
    ot, ct = open_mf, close_mf
    inline_tags = tags(p, "inline_formatting")
    if len(inline_tags) == 1:
        if "italics" in inline_tags:
            ot, ct = r"\textit{", "}"
        elif "smallcaps" in inline_tags:
            ot, ct = r"\textsc{", "}"
    for l in p.find("text").text.splitlines():
        l = l.strip()
        hyphen = False
        if len(l) and l[-1] == "-":
            hyphen = True
        l = text_to_latex(l)
        l = l.replace(open_mf, ot).replace(close_mf, ct)
        if hyphen:
            l += "%"
        out_lines.append(l)
    out_lines.append("%%%%%s%%%%" % p.attrib["id"])
    if "heading" in tags(p, "block_formatting"):
        process_heading(out_lines, heading_regexp)
    return "\n".join(out_lines)


def main():
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Usage: ", sys.argv[0], "rtt_file")
        sys.exit(-1)
    rtt = et.parse(sys.argv[1])
    pages = rtt.find("pages")
    os.chdir(os.path.dirname(sys.argv[1]))
    ei.include(pages)
    open_mf = pages.attrib["microformatting-open"]
    close_mf = pages.attrib["microformatting-close"]
    pages_text = []
    first_page_text = pages.find("page/text")
    if first_page_text.text[0] != "\n":
        first_page_text.text = "\n" + first_page_text.text
    for p in pages.findall("page"):
        pages_text.append(process_page(p, open_mf, close_mf, heading_regexp))
    sys.stdout.write("\n".join(pages_text))



if __name__ == "__main__":
    main()
