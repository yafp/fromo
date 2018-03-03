[![Code Health](https://landscape.io/github/yafp/fromo/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/fromo/master)
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)

![logo](https://raw.githubusercontent.com/yafp/fromo/master/img/fa-clock-o_64_0_000000_none.png) fromo
==========

# About
**fromo** is a python based toolset for logging the frontmost-window on Linux.

It contains:

- **fromo_logger.py** - logger which logs the frontmost command, windowtitle and PID.
- **fromo_analyzer.py** - analyzer which can generate a report out of the logger log file

## fromo_logger
![UI](https://raw.githubusercontent.com/yafp/fromo/master/img/Example_fromo_logger.png)

## fromo_analyzer
![UI](https://raw.githubusercontent.com/yafp/fromo/master/img/Example_fromo_analyzer.png)


# Requirements
The following packages are needed
- xdotool
- python (2.x)
- clint (python module - via: 'sudo pip install clint')


# Usage
## fromo_logger
- Mark as executable
```
chmod +x fromo_logger.py
```

- Start the logger script
```
./fromo_logger.py
```

The ```-h``` parameter shows optional parameters.



## fromo_analyzer
- Mark as executable
```
chmod +x fromo_analyzer.py
```

- Start the analyzer script
```
./fromo_analyzer.py
```

# Resources
* ASCII-Art was created using http://www.patorjk.com/software/taag with the Font Rectangle
