#!/usr/bin/python

"""
Output lines selected randomly from a file

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

import random, sys
from optparse import OptionParser

class randline:
    def __init__(self, list):
        
        self.lines = list
        
    #Added the withoutReplace parameter
    def chooseline(self, withoutReplace): 
        #If withoutReplace is on, delete lines
        if withoutReplace:
            current_line = random.choice(self.lines)
            self.lines.remove(current_line)
            return current_line
        else:
            return random.choice(self.lines)

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE
[-n], [--numlines]: enter number of random lines to output
[-u], [--unique]: modify file entries as unique, without repeats
[-w], [--without-replacement]: find random lines without any replacement
Output randomly selected lines from FILE."""

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-n", "--numlines",
                      action="store", dest="numlines", default=1,
                      help="output NUMLINES lines (default 1)")
    #Added the unique option
    parser.add_option("-u", "--unique",   
                      action="store_true", dest="unique", default=False,
                      help="ignore duplicate lines in the input")
    #Added the without-replacement option
    parser.add_option("-w", "--without-replacement",   
                      action="store_true", dest="withoutReplace", default=False,
                      help="output lines without replacement")

    options, args = parser.parse_args(sys.argv[1:])

    try:
        numlines = int(options.numlines)
        unique = bool(options.unique)
        withoutReplace = bool(options.withoutReplace)

    except:
        parser.error("invalid NUMLINES: {0}".
                     format(options.numlines))

    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
        if len(args) == 0:
            parser.error("At least one file is needed for evaluation")
    
    #In case of multiple files
    List_files = []
    for x in range(len(args)):
        F_t = open(args[x], 'r')
        L_t = F_t.readlines()
        if len(L_t) !=0 and L_t[-1][-1] != '\n': 
            #Add a new line if necessary
            L_t[-1] = L_t[-1] + '\n'
        #Concatenate to existing
        List_files = List_files + L_t 
        F_t.close()
    
    #In the case of unique (remove duplicates)
    if unique: 
        List_files = list(set(lineList))
    
    #Check if input file is empty
    if len(List_files) == 0:
        parser.error("Empty file(s)")

    #File to be used
    input_file = List_files
    
    try:
        #If -w option is on and not enough line entries
        if withoutReplace and numlines > len(List_files):
            parser.error("Must have no more than {0} lines".format(len(List_files)))
            sys.exit()
        generator = randline(input_file)
        for index in range(numlines):
            sys.stdout.write(generator.chooseline(withoutReplace))

    except IOError as no_err_str:
        parser.error("I/O error({0}): {1}".
                     format(no_err_str[0], no_err_str[1]))

if __name__ == "__main__":
    main()
