#!/usr/bin/python3

import xml.etree.ElementTree as et
import xml.etree.ElementInclude as ei
import sys

rtt = et.parse(sys.argv[1])
ei.include(rtt.getroot())
error_found = False
for page in rtt.findall(".//page"):
    messages = []
    img_lines = len(page.find("image/lines").text.split(","))
    text = page.find("text").text
    text_lines = len([X for X in text.splitlines() if len(X)])
    if(img_lines != text_lines):
        messages.append("Line count mismatch: image %d text %d" % (img_lines, text_lines))
    if text.find("'") != -1:
        messages.append("Single straight quote found")
    if text.find('"') != -1:
        messages.append("Double straight quote found")
    if text.find("--") != -1:
        messages.append("Double hyphen found")
    if messages:
        error_found = True
        print(page.attrib["id"])
        for m in messages:
            print("   ", m)
if not error_found:
    print("No errors found")
