#!/usr/bin/python3

import sys
import textwrap


tw = textwrap.TextWrapper(width=72, break_long_words=False)
wrap_style = "left"


def add_para(para, out):
    if wrap_style == "off":
        out.extend(para)
        out[-1] += "\n"
    else:
        #if wrap_style is not "off", then we don't want to
        #add a blank line for an empty paragraph
        if len(para) == 0: return
        unwrapped = "-"
        for l in para:
            if len(l) == 0: continue
            if unwrapped[-1] != "-" and l[0] != "-":
                unwrapped += " "
            unwrapped += l
        out.extend(tw.wrap(unwrapped[1:]))
        out[-1] += "\n"


def process_instruction(instruction, para, out):
    global wrap_style
    global tw
    fields = instruction.split()
    if fields[0] == "dowrap":
        add_para(para, out)
        del para[:]
    elif fields[0] == "blank":
        if para:
            add_para(para, out)
            del para[:]
        out[-1] += ("\n" * (int(fields[1]) - 1))
    elif fields[0] == "wrap":
        if para:
            add_para(para, out)
            del para[:]
        wrap_style = fields[1]
    elif fields[0] == "indent":
        if para:
            add_para(para, out)
            del para[:]
        tw.initial_indent = tw.subsequent_indent = " " * int(fields[1])


in_text = sys.stdin.read()
out = [""]
para = []
for l in in_text.splitlines():
    if l[:2] == "::" and l[-2:] == "::":
        process_instruction(l[2:-2], para, out)
    elif len(l) == 0:
        process_instruction("dowrap", para, out)
    else:
        para.append(l)
process_instruction("dowrap", para, out)
if out[0] == "": del out[0]
sys.stdout.write("\n".join(out).replace("\n", "\r\n"))

