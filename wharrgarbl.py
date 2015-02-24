#! /usr/bin/env python3
# -*- coding: utf-8 -*-

''' wharrgarbl.py -- Yet another word generator
    Generate (pseudo-)random pseudo-words based on weighted probabilities.
'''

# Copyleft 2013-15 Carsten Becker <carbeck@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import ast
import os.path
import random
import re
import sys

def wg_pick(rulelist):
    """
    Randomly pick an element from the rule list based on its associated probability.
    
    rulelist = ((item_0, p_item_0), (item_1, p_item_1), ..., (item_n, p_item_n))
    """
    
    # Sum up all the probability values in the group, i.e. there can be an
    # arbitrary number of each element in the group
    p_max = sum(p for i, p in rulelist)
    
    # Generate a random float number between 0.01 and p_max + 0.01 so that
    # 0.01 <= x < p_max + 0.01
    p = random.uniform(0.01, p_max + 0.01)
    
    # Loop through the elements while summing up their probabilities; if the
    # value of p is reached, exit the loop and return where we stopped
    p_cum = 0.0
    for item, p_item in rulelist:
        p_cum += p_item
        if p < p_cum:
            return item

def wg_rules(string):
    """
    Recursively iterate through the rule that is passed to the function.
    
    As long as rule variables ('{something}') can be found, search through the 
    string for instances of these, do search-and-replace on the first match, and
    reinsert the result into the string.
    """
    if not bool(re.search(r"{.*?}", string)):
        return string
    
    string = re.sub(r"{(.*?)}", lambda x: wg_pick(rulelist[x.group(1)]), string)
    return wg_rules(string)        

def main(argv=None):
    """Main function providing command line option parser and file I/O."""
    global rulelist
    if argv is None:
        argv = sys.argv[1:]
    
    # Construct parser and help texts for command-line arguments
    parser = argparse.ArgumentParser(prog="wharrgarbl.py", description=
                                     """Generate (pseudo-)random pseudo-words 
                                     based on weighted probabilities.""")
    parser.add_argument('rulelist', metavar='<rule list>', 
                        help="""File containing the generation rules.""")
    parser.add_argument('fileout', nargs='?', metavar='<output file>', 
                        help="""File to save the generated list of words in 
                        (optional)""")
    parser.add_argument('-n', '--number', nargs='?', default='10', type=int,
                        help="""The number of pseudo-words to be generated. If no 
                        value is "given, 10 will be assumed.""", metavar='N')
    parser.add_argument('-s', '--start', type=str, nargs='?', default='start', 
                        metavar='<start rule>', help='''The initial rule to 
                        kick off the generator, e.g. "begin" if your topmost 
                        rule is called "begin". If nothing is set, "start" will 
                        be assumed.''')
    
    args = parser.parse_args(argv)
    
    # Read input file; convert input into a list
    with open(args.rulelist, mode="r") as rules:
        rulelist = ast.literal_eval("{" + rules.read() + "}")
    
    # Generate the number of words provided by the command line input
    words = []
    for i in range(args.number):
        words.append(wg_rules("{" + args.start + "}"))
    
    # If a replacement ruleset is specified. NOTE: *must* be called "replace"!
    if "replace" in rulelist:
        for i, word in enumerate(words):
            for pattern, replacement in rulelist["replace"]:
                words[i] = re.sub(pattern, replacement, word)

    # If output is specified as a file, save to file
    if bool(args.fileout):
        with open(args.fileout, mode="w") as out:
            out.write("\n".join(sorted(words)))
    else:
        return "\n".join(sorted(words))

if __name__ == '__main__':
    sys.exit(main())
