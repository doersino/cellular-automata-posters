# TODO

Feature ideas and notes on potential *future work*:

* Use https://pypi.python.org/pypi/wolframalpha to get the entries of the "Properties" field from e.g. http://www.wolframalpha.com/input/?i=rule+30 and display them as "fun facts". Caveat: requires API key. Could add setting for API key, and only if that's present try to fetch fun facts.
* Add support for higher rules, e.g. http://www.wolframalpha.com/input/?i=rule+58008
* Improve label rendering code by moving all magic numbers to variables and making margins, border widths, font size etc. customizable.
* Write an equivalent script for Conway's Game of Life.
* Consider supporting continuous 1D automata: https://bitbucket.org/antonio_rt/1d-continuous-cellular-automata
* Add an option to use circles instead of squares? See https://www.reddit.com/r/cellular_automata/comments/6qchx5/python_script_generating_1d_cellular_automata/dkxg3n1/ for reference.

You're very welcome to send a pull request implementing one or more of the above (or file an issue if you have any other ideas for improvement)!
