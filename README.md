WHARRGARBL.PY
=============

Generate (pseudo-)random pseudo-words based on weighted probabilities with a little Python script.

Executing the Script
--------------------

You'll need Python 3 – I used version 3.4 to make this. Note that this is a *command-line program*. `python wharrgarbl.py -h` gives you some advice on the input:

    positional arguments:
      <rule list>           File containing the generation rules.
      <output file>         File to save the generated list of words in (optional)

    optional arguments:
      -h, --help            show this help message and exit
      -n [N], --number [N]  The number of pseudo-words to be generated. If no
                            value is "given, 10 will be assumed.
      -s [<start rule>], --start [<start rule>]
                            The initial rule to kick off the generator, e.g.
                            "begin" if your topmost rule is called "begin". If
                            nothing is set, "start" will be assumed.

Typical calls to the program will look like this:

    python wharrgarbl.py foo_rules.txt
    python wharrgarbl.py -n 25 bar_rules.txt
    python wharrgarbl.py -n 5 baz_rules.txt /home/johndoe/baz_out.txt
    python wharrgarbl.py -s begin qux_rules.txt


Rule Files
----------

Rule files are plain text files and should look like this:

    "W":(
        ("{C}{V}{C}{V}", 0.5),
        ("{C}{C}{V}{C}", 0.25),
        ("{C}{V}{V}", 0.25),
    ),
    
    "C":(
        ("p", 0.1),
        ("t", 0.16),
        ("k", 0.12),
        ("b", 0.04),
        ("m", 0.2),
        ("n", 0.16),
        ("ng", 0.12),
        ("v", 0.1)
    ),
    
    "V":(
        ("i", 0.18),
        ("e", 0.1),
        ("a", 0.2),
        ("o", 0.08),
        ("u", 0.04),
        ("{X}", 0.4)
    ),
    
    "X":(
        ("ay", 0.5),
        ("ey", 0.5)
    )

In more general terms, a rule has the following form:

    "rule_name":(
        ("element", <probability>)
    )
    
Inside an ("element", ‹probability›) couple, "element" can contain the name
of a rule itself again:

    ("{rule_name}", <probability>)
    
Mixing rule names with non-rules is no problem:

    "X":(
        ("a{L}a", 0.25),
        ("a{F}a", 0.75)
    ),
    "L":(
        ("r", 0.5),
        ("l", 0.5)
    ),
    "F":(
        ("s", 0.5),
        ("f", 0.25),
        ("x", 0.25)
    )

You can also match and replace by Python-compatible regular expressions, e.g.

    "replace":(
        (r"(\w)b\1", r"b\1")
    )

This will replace a word-character `\w` followed by `b` and followed by the 
same character `\w` again with just `b` and the character, e.g. `aba` will be 
replaced with `ba`.


Disclaimer
----------

This software comes "as-is" with no warranties expressed or implied. The bulk of the program was written in November 2013 while I was taking an intro class on Python at the Lingustics department of University of Marburg, Germany. Corrections and improvements, especially regarding noob errors, are always welcome!
