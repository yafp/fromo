[![Code Health](https://landscape.io/github/yafp/fromo/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/fromo/master)
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)

![logo](https://raw.githubusercontent.com/yafp/fromo/master/img/fa-clock-o_64_0_000000_none.png) fromo
==========

# About
**fromo** is a python based toolset for logging the frontmost-window on Linux.

It contains:

- **fromoL.py** - logger which logs the frontmost, its command, windowtitle and PID.
- **fromoA.py** - analyzer which can generate a report out of the log file

## fromoL
![UI](https://raw.githubusercontent.com/yafp/fromo/master/img/Example_fromoL.png)

## fromoA
![UI](https://raw.githubusercontent.com/yafp/fromo/master/img/Example_fromoA.png)


# Requirements
The following packages are needed
- wmctrl
- xprop
- python (2.x)
- clint (python module - via: 'sudo pip install clint')


# Setup
## Logger (fromoL.py)
- Open fromoL.py and configure the values in the CONFIG block
- Start the logger script (fromoL.py) manually or via cronjob

## Analyzer (fromoA.py)
- Start the analyzer script (fromoA.py) manually or via cronjob
- Have fun with the generated .html reports


# Resources
ASCII-Art was created using http://www.patorjk.com/software/taag with the Font Rectangle
