#!/usr/bin/python

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys
from optparse import OptionParser

class randline:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()
    
    #Added a 2nd parameter "withoutReplacement" as a boolean for -w
    def chooseline(self, withoutReplacement):
        #If 'withoutReplacemement' is true, the line chosen will be removed 
        #and it won't be possible to choose it again
        if withoutReplacement:
            printout = random.choice(self.lines)
            self.lines.remove(printout)
            return printout
        else:
            return random.choice(self.lines)

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE

Output randomly selected lines from FILE."""

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-n", "--numlines",
                      action="store", dest="numlines", default=1,
                      help="output NUMLINES lines (default 1)")

    #Added the option for -u which ignores duplicate lines
    parser.add_option("-u", "--unique", 
                     action="store_true", dest="unique", default=0,
                     help="Ignores duplicate lines in the input")

    #Added the option for -w to output lines w/o replacement
    parser.add_option("-w", "--without-replacement", 
                      action="store_true", dest="withoutReplacement", default=0,
                      help="Outputs lines without replacement")

    options, args = parser.parse_args(sys.argv[1:])  #args acts as an array

    try:
        numlines = int(options.numlines)
    except:
        parser.error("invalid NUMLINES: {0}".
                     format(options.numlines))

    #Add destination files when adding options via parse:
    try:
        unique = bool(options.unique)
    except: 
        parser.error("invalid UNIQUE")
    
    try:
        withoutReplacement = bool(options.withoutReplacement)
    except:
        parser.error("invalid WITHOUT_REPLACEMENT")

    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
    if len(args) < 1: #Take any arbitrary positive # of input file arguments
        parser.error("Please provide at least 1 argument")

    #Checking for multiple files
    arr = []  #Make an array to keep track of all the lines
    for i in args: 
        read_file = open(i, 'r') #Open files in the list of type 'read'
        temp_file = read_file.read() #Store the read file as a temporary file

        if (len(temp_file) is 0):
           parser.error("Cannot have empty file")
        if temp_file.endswith("\n") is False: 
       #If the last element is not a new line, add a new line
            temp_file += "\n"
        #Concatenate to any previous files if necessary
        for i in temp_file.split():
            arr.append(i)
        read_file.close()

    #-u condition: Ignore duplicate lines
    if unique:
        arr = list(set(arr))  #Typecast into a set to get rid of duplicates
                              #then typecast it back to its original form

    #If -w is true and there are not enough line entries to fulfill the request
    if withoutReplacement and len(arr) < numlines:
        parser.error("Must have no more than {0} lines".format(len(arr)))

    #sanity check to see if output is correct into a temporary text file
    empty_str = ""
    for j in arr:
        empty_str += (j + "\n")
    x = open("temp", 'w')
    x.write(empty_str)
    x.close()    
    #end sanity check

    try:
        generator = randline("temp")
        for index in range(numlines):
            sys.stdout.write(generator.chooseline(withoutReplacement))
    except IOError as packed:
        parser.error("I/O error({0}): {1}".
                     format(packed.errno, packed.strerror))

if __name__ == "__main__":
    main()
