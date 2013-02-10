#!/usr/bin/python3

import xml.etree.ElementTree as et
import xml.etree.ElementInclude as ei
import sys

rtt = et.parse(sys.argv[1])
ei.include(rtt.getroot())
for page in rtt.findall(".//page"):
    img_lines = page.find("image/lines").text.split(",")
    text_lines = [X for X in page.find("text").text.splitlines() if len(X)]
    if(len(img_lines) != len(text_lines)):
        print(page.attrib["id"], "Image", len(img_lines), "Text", len(text_lines))

