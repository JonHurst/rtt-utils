#!/usr/bin/python3

#usage: rtt2xhtml.py rtt_file

import sys
import os
import xml.etree.ElementTree as et
import xml.etree.ElementInclude as ei
import html
import re

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


def process_page(p, open_mf, close_mf, contents):
    global chapter_counter
    out_lines = []
    hdg = False
    if "heading" in tags(p, "block_formatting"):
        hdg = "o"
    ot, ct = open_mf, close_mf
    inline_tags = tags(p, "inline_formatting")
    if len(inline_tags) == 1:
        if "italics" in inline_tags:
            ot, ct = "<i>", "</i>"
        elif "smallcaps" in inline_tags:
            ot, ct = "<span class='sc'>", "</span>"
    for l in p.find("text").text.splitlines():
        l = l.strip()
        if l == "":
            if hdg == "o":
                out_lines.append("</p></div><div class='chapter' id='ch%d'><h1>" % chapter_counter)
                hdg = "c"
            elif hdg == "c":
                out_lines.append("</h1><p>")
                chapter_counter += 1
                hdg = False
            else:
                out_lines.append("</p><p>")
        else:
            l = html.escape(l, False)
            l = l.replace(open_mf, ot).replace(close_mf, ct)
            if hdg == "c":
                contents.append("<li><a href='#ch%d'>%s</a></li>" % (chapter_counter, l))
            out_lines.append(l)
    out_lines.append("<!--%s-->" % p.attrib["id"])
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
    contents = []
    pages_text = []
    for p in pages.findall("page"):
        pages_text.append(process_page(p, open_mf, close_mf, contents))
    contents_html = contents_template % "\n".join(contents)
    pages_html = "\n".join(pages_text) + "\n</p></div>"
    mo = re.search(r"<[^/]", pages_html)
    sys.stdout.write(file_template % (contents_html + pages_html[mo.start():]))




if __name__ == "__main__":
    main()
