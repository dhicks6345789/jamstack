#!/usr/bin/python3

# Standard libraries.
import os
import sys

def tidyHTML(rootPath):
    for item in os.listdir(rootPath):
        if os.path.isdir(rootPath + os.sep + item):
            tidyHTML(rootPath + os.sep + item)
        else:
            if item.lower().endswith("html"):
                print("Tidying: " + rootPath + os.sep + item)
                output = ""
                infile = open(rootPath + os.sep + item, encoding="latin-1")
                for inputLine in infile.readlines():
                    if not inputLine.strip() == "":
                        output = output + inputLine
                infile.close()
                outfile = open(rootPath + os.sep + item, "wt", encoding="utf-8")
                outfile.write(output)
                outfile.close()
                
if len(sys.argv) >= 2:
    tidyHTML(sys.argv[1])
else:
    print("TidyHTML - tidy all HTML files in a folder and sub folders.")
    print ("Usage: tidyHTML rootFolder")
