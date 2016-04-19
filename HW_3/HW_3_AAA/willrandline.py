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

                                        def chooseline(self, without):
                                                    #if without is true, remove that line once it is chosen
                                                            #so it can't be chosen again
                                                            if without == True:
                                                                            output = random.choice(self.lines)
                                                                                        self.lines.remove(output)
                                                                                                    return output
                                                            else:
                                                                            return random.choice(self.lines)

                                                                        def main():
                                                                                version_msg = "%prog 2.0"
                                                                                    usage_msg = """%prog [OPTION]... FILE

Output randomly selected lines from FILE.
-u will ignore duplicates in the input
-w will not repeat the same line as output"""

                                                                                        parser = OptionParser(version=version_msg,
                                                                                                                                        usage=usage_msg)
                                                                                            parser.add_option("-n", "--numlines",
                                                                                                                                    action="store", dest="numlines", default=1,
                                                                                                                                    help="output NUMLINES lines (default 1)")
                                                                                                parser.add_option("-u", "--unique",
                                                                                                                                        action="store_true", dest="unique", default=False,
                                                                                                                                        help="duplicate lines are ignored")
                                                                                                    parser.add_option("-w", "--without-replacement",
                                                                                                                                            action="store_true", dest="without", default=False,
                                                                                                                                            help="output lines without repeating")

                                                                                                    options, args = parser.parse_args(sys.argv[1:])

                                                                                                    try:
                                                                                                                numlines = int(options.numlines)
                                                                                                    except:
                                                                                                                parser.error("invalid NUMLINES: {0}".
                                                                                                                                                  format(options.numlines))
                                                                                                                try:
                                                                                                                            unique = bool(options.unique)
                                                                                                                except:
                                                                                                                            parser.error("invalid UNIQUE")

                                                                                                                            try:
                                                                                                                                        without = bool(options.without)
                                                                                                                            except:
                                                                                                                                        parser.error("invalid WITHOUT")

                                                                                                                                        if numlines < 0:
                                                                                                                                                    parser.error("negative count: {0}".
                                                                                                                                                                                      format(numlines))
                                                                                                                                                    if len(args) < 1:
                                                                                                                                                                parser.error("wrong number of operands")

                                                                                                                                                                    #create an empty array
                                                                                                                                                                        wordlist = []

                                                                                                                                                                            #fill wordlist with lines from an arbitrary num of files
                                                                                                                                                                            for i in args:
                                                                                                                                                                                        f = open(i, 'r')
                                                                                                                                                                                                tempfile = f.read()
                                                                                                                                                                                                        #add a newline if a line doesn't have one
                                                                                                                                                                                                        if tempfile.endswith("\n") == False:
                                                                                                                                                                                                                        tempfile = tempfile + "\n"
                                                                                                                                                                                                                                #add each individual line as an element to wordlist
                                                                                                                                                                                                                                for i in tempfile.split():
                                                                                                                                                                                                                                                wordlist.append(i)
                                                                                                                                                                                                                                                        f.close()

                                                                                                                                                                                                                                                            #if -u is used, remove duplicates
                                                                                                                                                                                                                                                            if unique == True:
                                                                                                                                                                                                                                                                        wordlist = list(set(wordlist))
                                                                                                                                                                                                                                                                                #for the case where duplicates are removed and
                                                                                                                                                                                                                                                                                        #there would not be enough lines to fulfill the numlines requested
                                                                                                                                                                                                                                                                                        if (len(wordlist) < numlines and without == True):
                                                                                                                                                                                                                                                                                                        parser.error("Number of input lines are fewer than requested.")

                                                                                                                                                                                                                                                                                                            #create a string from the list
                                                                                                                                                                                                                                                                                                                words_string = ""
                                                                                                                                                                                                                                                                                                                for i in wordlist:
                                                                                                                                                                                                                                                                                                                            words_string += (i + "\n")

                                                                                                                                                                                                                                                                                                                                #print words_string

                                                                                                                                                                                                                                                                                                                                    #create a file containing the lines
                                                                                                                                                                                                                                                                                                                                        input_file = open("temporary", 'w')
                                                                                                                                                                                                                                                                                                                                            input_file.write(words_string)
                                                                                                                                                                                                                                                                                                                                                input_file.close()

                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                            generator = randline("temporary")
                                                                                                                                                                                                                                                                                                                                                            for index in range(numlines):
                                                                                                                                                                                                                                                                                                                                                                            sys.stdout.write(generator.chooseline(without))
                                                                                                                                                                                                                                                                                                                                                except IOError as err:
                                                                                                                                                                                                                                                                                                                                                            parser.error("I/O error({0}): {1}".
                                                                                                                                                                                                                                                                                                                                                                                              format(err.errno, err.strerror))

                                                                                                                                                                                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                                                    main()
