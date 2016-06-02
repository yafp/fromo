[![Code Health](https://landscape.io/github/yafp/fromo/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/fromo/master)
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)

![logo](https://raw.githubusercontent.com/yafp/fromo/master/img/fa-clock-o_64_0_000000_none.png) fromo
==========

# About
**fromo** is a python based toolset for logging the frontmost-window on Linux.

It contains:

- fromol - logger which periodically for the currently frontmost window and logs its command title and PID.
- fromoa - analyzer which can generate a report out of the log file


# Requirements
The following packages are needed
- wmctrl
- xprop
- python
- clint (python module)

Install clint via

> sudo pip install clint


# Installation
TODO: makefile


# Setup and configure the logger
- Open fromol.py and configure the values in the CONFIG block
- Start the main script (fromo.py) manually or via cronjob
Optional:
- Configure logrotation via logrotate
