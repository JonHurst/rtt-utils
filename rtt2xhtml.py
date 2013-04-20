#!/usr/bin/python3

#usage: rtt2xhtml.py rtt_file

import sys
import os
import xml.etree.ElementTree as et
import xml.etree.ElementInclude as ei
import html
import re
import argparse

chapter_counter = 0


file_template = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title></title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
  </head>
  <body>
%s
  </body>
</html>"""


contents_template = """\
<div class='contents'>
<h1>Contents</h1>
<ul>%s</ul>
</div>
"""


def tags(p, t):
    retval = set()
    tags = p.find("tags[@class='%s']" % t)
    if tags == None: return retval
    for tag in tags.findall("tag"):
        retval.add(tag.text)
    return retval


def process_heading(out_lines, contents, heading_regexp, heading_blocks):
    global chapter_counter
    #find the line containing the heading
    if heading_regexp == "":
        hdg = re.compile(r"\w+")
    else:
        hdg = re.compile(heading_regexp)
    prev_blank, next_blank, hdg_line = -1, -1, -1
    for c, l in enumerate(out_lines):
        if l == "</p><p>":
            prev_blank = c
        elif hdg.search(l):
            hdg_line = c
            break
    if hdg_line == -1: return
    contents_str = out_lines[hdg_line]
    if heading_blocks > 1: multi_block_heading = True
    sub = False
    while heading_blocks:
        c += 1
        if out_lines[c] != "</p><p>":
            contents_str += " " + out_lines[c]
            continue
        if heading_blocks > 1:
            if sub:
                out_lines[c] = "<br/>"
            else:
                out_lines[c] = '<br/><span class="sub">'
                sub = True
        else:
            if sub:
                out_lines[c] = out_lines[c].replace("</p>", "</span></h2>")
            else:
                out_lines[c] = out_lines[c].replace("</p>", "</h2>")
        heading_blocks -= 1
    if chapter_counter == 0:
        open_str = "<div class='chapter' id='ch%d'><h2>" % chapter_counter
    else:
        open_str = "</div><div class='chapter' id='ch%d'><h2>" % chapter_counter
    if prev_blank == -1:
        out_lines.insert(0, open_str)
    else:
        out_lines[prev_blank] = out_lines[prev_blank].replace("<p>", open_str)
    contents.append("<li><a href='#ch%d'>%s</a></li>" % (chapter_counter, contents_str))
    chapter_counter += 1


def process_page(p, open_mf, close_mf, contents, heading_regexp="", heading_blocks=1):
    out_lines = []
    pid = p.attrib["id"]
    noted_lines = set()
    for n in p.findall("notes/note"):
        if "line" in n.attrib:
            noted_lines.add(int(n.attrib["line"]))
    #process easy inline formatting
    ot, ct = open_mf, close_mf
    inline_tags = tags(p, "inline_formatting")
    if len(inline_tags) == 1:
        if "italics" in inline_tags:
            ot, ct = "<i>", "</i>"
        elif "smallcaps" in inline_tags:
            ot, ct = "<span class='sc'>", "</span>"
    for c, l in enumerate(p.find("text").text.splitlines()):
        l = l.strip()
        a = ""
        if c + 1 in noted_lines:
            a = "<a id='p%sl%d'/>" % (pid, c)
        if l == "":
            out_lines.append(a + "</p><p>")
        else:
            l = html.escape(l, False)
            l = l.replace(open_mf, ot).replace(close_mf, ct)
            l = l.replace(" ”", " ”") #prevent line breaking between – and ”
            l = l.replace(": –", ": –") #prevent line breaking between : and –
            out_lines.append(a + l)
    out_lines.append("<!--%s-->" % p.attrib["id"])
    if "heading" in tags(p, "block_formatting"):
        process_heading(out_lines, contents, heading_regexp, heading_blocks)
    return "\n".join(out_lines)


def main():
    parser = argparse.ArgumentParser(description='Create xhtml from rtt.')
    parser.add_argument("rtt_file", help="RTT file.")
    parser.add_argument("-r", "--heading_regexp", help="Regexp to identify a chapter heading")
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
    contents = []
    pages_text = []
    first_page_text = pages.find("page/text")
    if first_page_text.text[0] != "\n":
        first_page_text.text = "\n" + first_page_text.text
    for p in pages.findall("page"):
        pages_text.append(process_page(p, open_mf, close_mf,
                                       contents, args.heading_regexp, args.heading_blocks))
    contents_html = contents_template % "\n".join(contents)
    pages_html = "\n".join(pages_text) + "\n</p></div>"
    pages_html = pages_html.replace("-\n", "-<!--\n-->")
    mo = re.search(r"<[^/]", pages_html)
    sys.stdout.write(file_template % (contents_html + pages_html[mo.start():]))




if __name__ == "__main__":
    main()
