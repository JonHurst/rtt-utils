#!/usr/bin/python3

import sys
import xml.etree.ElementTree as et
import os
import glob

rtt_template = """\
<?xml version='1.0' encoding='utf-8'?>
<book xmlns:xi="http://www.w3.org/2001/XInclude">
  <title> </title>
  <subtitle> </subtitle>
  <author> </author>
  <edition> </edition>
  <pages microformatting-close="}}" microformatting-open="{{">
    <!-- <page id="003"> -->
    <!--   <image src="http://www.gutenberg.org/files/41445/41445-page-images/p0003.png"><lines>222,1828,2168,2451,2755,3056,3391,3691,3996,4296,4566,4902,5176,5528,5833,6147,6438,6743,7048,7353,7653,7966,8262,8572,8876,9185,9455,9791</lines></image> -->
    <!--   <text><xi:include href="text/003" parse="text" /></text> -->
    <!-- </page> -->
  </pages>
</book>
"""


def make_page(ident, text_file, image_file):
    page = et.Element("page", {"id": ident})
    img = et.Element("image", {"src": image_file})
    page.append(img)
    text = et.Element("text")
    inc = et.Element("{http://www.w3.org/2001/XInclude}include",
                     {"href": text_file,
                      "parse": "text"})
    text.append(inc)
    page.append(text)
    return page


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
        not os.path.isdir(sys.argv[1]) or
        not os.path.isdir(sys.argv[2])):
        print("Usage: %s text_dir image_dir" % sys.argv[0])
        sys.exit(-1)
    text_files = glob.glob(sys.argv[1] + "/*")
    text_files.sort()
    image_files = glob.glob(sys.argv[2] + "/*")
    image_dict = {}
    for i in image_files:
        bn = os.path.basename(i)
        (root, ext) = os.path.splitext(bn)
        image_dict[root] = i
    et.register_namespace("xi", "http://www.w3.org/2001/XInclude")
    rtt = et.XML(rtt_template)
    pages = rtt.find("pages")
    for t in text_files:
        bn = os.path.basename(t)
        (root, ext) = os.path.splitext(bn)
        if root in image_dict:
            pages.append(make_page(root, t, image_dict[root]))
        else:
            print("No entry made for", t, file=sys.stderr)
    indent(rtt)
    et.ElementTree(rtt).write(sys.stdout, encoding="unicode", xml_declaration=True)


if __name__ == "__main__":
    main()
