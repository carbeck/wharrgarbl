#! /usr/bin/env python 
# -*- coding: utf-8 -*-

''' wharrgarbl.py -- Yet another word generator

    Generate (pseudo-)random pseudo-words based on weighted probabilities.
'''

# Copyleft 2013 Carsten Becker <carbeck@gmail.com>
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
import codecs
import os
import os.path
import random
import re
import sys

# Pick element from the rule list based on its associated probability
# rulelist = ((item_0, p_item_0), (item_1, p_item_1), ..., (item_n, p_item_n))
def wg_pick(rulelist):
    """Randomly pick an element from a list based on the element's probability."""
    p = random.uniform(0,1)
    p_cum = 0.0
    for item, p_item in rulelist:
        p_cum += p_item
        if p < p_cum:
            return item

# Takes matches and replaces them with a randomly picked rule from the rule list
def wg_replacerule(matchobj):
    """Replace the match with a randomly picked element from the rule definitions."""
    string = matchobj.group(1)
    return wg_pick(rulelist[string])

# Recursively walk through the rule list
def wg_rules(string):
    """As long as rule variables can be found, search through the string."""
    if bool(re.search(r"{.*?}", string)) == True:
        string = re.sub(r"{(.*?)}", wg_replacerule, string)
        return wg_rules(string)
    else:
        return string

# Main
def main(argv=None):
    """Main function providing command line option parser etc."""
    global rulelist
    if argv is None:
        argv = sys.argv[1:]
    
    # Construct parser and help texts for command-line arguments
    parser = argparse.ArgumentParser(prog="wharrgarbl.py", description=
                "Generate (pseudo-)random pseudo-words based on weighted probabilities.")
    parser.add_argument('-n', '--number', nargs='?', default='10', type=int, 
            help="The number of pseudo-words to be generated. If no value is "
            "given, 10 will be assumed.", metavar='N')
    parser.add_argument('-r', '--rules', dest='rulelist', required=True, 
            help="File containing the generation rules.", metavar='<file>')
    parser.add_argument('-o', '--out', dest='fileout', metavar='<file>',
            help="File to save the generated list of words in (optional)")
    parser.add_argument('start', type=str, metavar='<start_string>',
            help="The initial rule to kick off the generator, "
            'e.g. "{W}" if your topmost rule is called "W".')
    
    args = parser.parse_args(argv)
    
    # Read input file; convert input into a list
    with codecs.open(args.rulelist, mode="r") as rules:
        rulelist = ast.literal_eval("{" + rules.read() + "}")
    
    # Generate number of words provided by command line
    words = ''
    for i in xrange(args.number):
        words += "{}\n".format(wg_rules(args.start))
    
    # If output is specified as a file, save to file, else print to shell
    if bool(args.fileout) == True:
        with codecs.open(args.fileout, mode="w") as out:
            out.write("{}".format(words))
    else:
        return words

if __name__ == '__main__':
    sys.exit(main())
