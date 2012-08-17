## Summary
PythonFormat is a python formatting plugin for Sublime Text 2.

## Features
* Turns `"`double quotes`"` into `'`single quotes`'` where possible
* Adds spacing around mathematical operators.
	- `print 2+-4/3` will become `print 2 + -4 / 3`
* Adds spacing around syntactically valid statements. 
	- `do_method(arg1,arg2,arg3)` will become `do_method(arg1, arg2, arg3)` 
	- `if(True):` will become `if (True):`
	- `print'Hello, World'` will become `print 'Hello, World'`
* Adds parentheses around `if`, `elif`, and `while` statements
* Intelligently wraps lines enclosed in parentheses/braces/brackets
* Intelligently wraps comments
* Enforces a maximum of 2 new lines in a row
* Trims excess white space  

## Installation
Clone this repository in to the Sublime Text 2 "Packages" directory, which is located wherever the "Preferences" -> "Browse Packages" option in sublime takes you. A restart of Sublime may be necessary.

## Usage
The default key binding is `super+shift+f`. Alternatively, you can do open the command pallette via `super+shift+p` and enter "Format: Python". This will format your entire opened file. Currently, there is no support for formatting of a highlighted selection.

## Should I use PythonFormat or PythonTidy?
I have another Sublime Text 2 plugin, called [SublimePythonTidy](https://github.com/davidleibovic/SublimePythonTidy). It is based on the formatting provided by the excellent [PythonTidy](http://pypi.python.org/pypi/PythonTidy) script. 

SublimePythonTidy will be more reliable and less likely to screw up your code, as it uses a more mature, better tested formatter. SublimePythonTidy works by parsing the abstract syntax tree of your Python code. As such, it requires the file being formatted to be valid Python syntax. If you forgot to insert a colon or some other symbol, SublimePythonTidy will not be able to run. PythonFormat, on the other hand, will still make an attempt at formatting your code, even if it is not valid Python syntax.

Here is a sample of how the formatting style compares (I personally happen to prefer the style used by PythonFormat).

### Input:
    if self.opts.max_preserve_newlines == 0 or self.opts.max_preserve_newlines > self.n_newlines:
### PythonFormat Output:
    if (self.opts.max_preserve_newlines == 0 or
        self.opts.max_preserve_newlines > self.n_newlines):
### SublimePythonTidy Output:
    if self.opts.max_preserve_newlines == 0 \
        or self.opts.max_preserve_newlines \
        > self.n_newlines:

### Input:
    self.operators = ['!=', '%', '&', '*', '**', '+', '+=', '-=', '-', '/','//', '<', '<<', '<=', '~', '==', '=', '>', '>=', '>>','^', '|', '<>', '*=', '/=', '%=', '**=', '//=', '|=','&=', '^=']
### PythonFormat Output:
    self.operators = ['!=', '%', '&', '*', '**', '+', '+=', '-=', '-', '/',
                      '//', '<', '<<', '<=', '~', '==', '=', '>', '>=', '>>',
                      '^', '|', '<>', '*=', '/=', '%=', '**=', '//=', '|=',
                      '&=', '^=']
### SublimePythonTidy Output:
	self.operators = [
            '!=',
            '%',
            '&',
            '*',
            '**',
            '+',
            '+=',
            '-=',
            '-',
            '/',
            '//',
            '<',
            '<<',
            '<=',
            '~',
            '==',
            '=',
            '>',
            '>=',
            '>>',
            '^',
            '|',
            '<>',
            '*=',
            '/=',
            '%=',
            '**=',
            '//=',
            '|=',
            '&=',
            '^=',
            ]

## Disclaimer
PythonFormat has been tested, but it is still very new! There is a real chance it could screw up your files, so be careful, test, and save a backup.

