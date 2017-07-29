# TODO

Feature ideas and notes on potential *future work*:

* Use https://pypi.python.org/pypi/wolframalpha to get the entries of the "Properties" field from e.g. http://www.wolframalpha.com/input/?i=rule+30 and display them as "fun facts". Caveat: requires API key. Could add setting for API key, and only if that's present try to fetch fun facts.
* Add support for higher rules, e.g. http://www.wolframalpha.com/input/?i=rule+58008
* Improve label rendering code by moving all magic numbers to variables and making margins, border widths, font size etc. customizable.
* Allow roatation of the grid by some small angle. Might make things more visually interesting, but increase code complexity due to having to increase the canvas dimensions based on the angle to cover page.
* Write an equivalent script for Conway's Game of Life.

You're very welcome to send a pull request implementing one or more of the above (or file an issue if you have any other ideas for improvement)!
