# Sublime IPython Pick

Adds a command for selecting one of the last statements in `ipython_log.py` and inserting it at caret position.

How it works
------------

While using [IPython](http://ipython.org) you can activate the log functionality
with [%logstart](http://ipython.org/ipython-doc/stable/interactive/magics.html#magic-logstart).
That will save all your commands to a file named `ipython_log.py` (by default).

The command will search for that file, first in the current project root (if you're using one),
and then in each directory that contains the current open file, climbing the file system hierarchy.

Once found, the last statements are extracted, filtered and listed in a drop-down.
Selecting one of them inserts it at caret position.

The statements are filtered by removing:

  * calls to IPython magic commands
  * repeated statements
  * reassignments to the same variable: only the last assignment to a given variable is kept.


Limitations
-----------

* The package currently only supports the default log file name `ipython_log.py`.
* The maximum number of statements is hard coded (30 statements).


Usage
-----

* (Suggestion) Bind the command  `ipython_pick` to some key in your Key Bindings, e.g.

        { "keys": ["ctrl+alt+a"], "command": "ipython_pick" },

* Activate the command
* Select a statement from the drop-down that appears
* The statement is inserted at the caret position


Future improvements
-------------------

* make the maximum number of statements configurable
* insert import statements at the right position at the top of the file
* select a group of statements at once
