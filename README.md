## Summary
PythonFormat is a python formatting plugin for Sublime Text 2.

## Features
* Turns "double quotes" into 'single quotes' where possible
* Adds spacing around mathematical operators.
	- *print 2+-4/3* will become *print 2 + -4 / 3*
* Adds spacing around syntactically valid statements. 
	- *do_method(arg1,arg2,arg3)* will become *do_method(arg1, arg2, arg3)* 
	- *if(True):* will become *if (True):*
	- *print'Hello, World'* will become *print 'Hello, World'*
* Adds parentheses around if, elif, and while statements
* Intelligently wraps lines enclosed in parentheses/braces/brackets
* Intelligently wraps comments
* Enforces a maximum of 2 new lines in a row
* Trims excess white space  

## Installation
Clone this repository in to the Sublime Text 2 "Packages" directory, which is located wherever the "Preferences" -> "Browse Packages" option in sublime takes you. A restart of Sublime may be necessary.

## Usage
The default key binding is "super+shift+f". Alternatively, you can do open the command pallette via "super+shift+p" and enter "Format: Python". This will format your entire opened file. Currently, there is no support for formatting of a highlighted selection.

## Disclaimer
PythonFormat has been tested, but it is still very new! There is a real chance it could screw up your files, so be careful, test, and save a backup.

