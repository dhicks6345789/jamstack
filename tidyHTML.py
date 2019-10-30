#!/usr/bin/python3

# Standard libraries.
import os
import sys

def tidyHTML(rootPath, pathsToIgnore):
    for pathToIgnore in pathsToIgnore:
        if (rootPath + os.sep).startswith(pathToIgnore):
            return
    for item in os.listdir(rootPath):
        if os.path.isdir(rootPath + os.sep + item):
            tidyHTML(rootPath + os.sep + item, pathsToIgnore)
        else:
            if item.lower().endswith("html"):
                print("Tidying: " + rootPath + os.sep + item)
                output = ""
                infile = open(rootPath + os.sep + item)
                #previousLineBlank = False
                for inputLine in infile.readlines():
                    if not inputLine.strip() == "":
                        output = output + inputLine
                    #if inputLine.strip() == "":
                        #if not previousLineBlank:
                            #output = output + inputLine
                        #previousLineBlank = True
                    #else:
                        #output = output + inputLine
                        #previousLineBlank = False
                infile.close()
                outfile = open(rootPath + os.sep + item, "wt", encoding="utf-8")
                outfile.write(output)
                outfile.close()
                
if len(sys.argv) >= 2:
    ignorePaths = []
    for pl in range(2, len(sys.argv)):
        ignorePaths.append(sys.argv[pl])
    tidyHTML(sys.argv[1], ignorePaths)
else:
    print("TidyHTML - tidy all HTML files in a folder and sub folders.")
    print ("Usage: tidyHTML rootFolder ignorePaths...")