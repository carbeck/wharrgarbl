WHARRGARBL.PY
=============

Generate random pseudo-words based on weighted probabilities with a little Python script.

Executing the Script
--------------------

You'll need Python – I used version 2.7.3 to make this. Note that this is a *command-line program*. `python wordgen.py -h` gives you some advice on the input:

    positional arguments:
      <start_string>        The initial rule to kick off the generator, e.g. "{W}"
                            if your topmost rule is called "W".
    
    optional arguments:
      -h, --help            show this help message and exit
      -n [N], --number [N]  The number of pseudo-words to be generated. If no
                            value is given, 10 will be assumed.
      -r <file>, --rules <file>
                            File containing the generation rules.
      -o <file>, --out <file>
                            File to save the generated list of words in (optional)

Rule files
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
    
Inside an ("element", <probability>) couple, "element" can contain the name
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

Disclaimer
----------

This software comes "as-is" with no warranties expressed or implied.
