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

    def chooseline(self):
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

    options, args = parser.parse_args(sys.argv[1:])  #args is an array

    try:
        numlines = int(options.numlines)
        #Add destination files when adding options via parse:
        unique = bool(options.unique)
        withoutReplacement = bool(options.withoutReplacement)

    except:
        parser.error("invalid NUMLINES: {0}".
                     format(options.numlines))
    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
    if len(args) < 1: #Take any arbitrary positive # of input file arguments
        parser.error("Please provide at least 1 argument")
    input_file = args[0]

    #Checking for multiple files
    arr = []  #Make an array to keep track of all the lines
    for i in range(len(args)): 
        read_file = open(args[i], 'r') #Open files in the list of type 'read'
        read_line = read_file.readlines() #Read 1 line at a time w/ readlines()
        if len(arr) == 0 or arr[len(arr) - 1] != '\n': 
       #If array is empty or the last element is not a new line, add a new line
            arr.append('/n')
        #Concatenate to any previous files if necessary
        arr += read_line
        read_file.close()

    #-u condition: Ignore duplicate lines
    if unique:
        read_line = list(set(arr))

    #-w condition: Output lines without replacement
    if withoutReplacement:
        TEST = 1

    try:
        generator = randline(input_file)
        for index in range(numlines):
            sys.stdout.write(generator.chooseline())
    except IOError as (errno, strerror):
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
