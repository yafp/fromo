#!/usr/bin/env python2
# coding=utf-8
# Name:			fromo_analyzer.py
# Function:		Analyzer - analyzes the fromo_logger log 
#               and generates some kind of report
# URL:          https://github.com/yafp/fromo
# Author: 		https://github.com/yafp/
#               http://yafp.de
#
# Resources:
#               http://stackoverflow.com/questions/26485621/read-a-text-file-in-python-line-wise

""" fromo_analyzer - The fromo analyzer component """


################################################################################
# IMPORTS
################################################################################
import os
import sys
from clint.textui import colored, puts  # for colored text
# fromo imports
import fromo_utils as u
import fromo_constants as c


################################################################################
# CONSTANT
################################################################################


################################################################################
# ARRAY DEFINITION
################################################################################
arr_new_lines = []
arr_dates = []
arr_commands = []
arr_titles = []
arr_pids = []


################################################################################
# READING LOG
################################################################################
if sys.platform == "linux" or sys.platform == "linux2": # check if platform is supported or not
    os.system('clear')  # # clear the screen

    print " ___                   _____ "
    print "|  _|___ ___ _____ ___|  _  |"
    print "|  _|  _| . |     | . |     |"
    print "|_| |_| |___|_|_|_|___|__|__|    Version:"+str(c.VERSION)+"\n"

    print "Starting reading log ..."
    fromolLogFile = open("fromo.log", "r") # open the log file

    # read it linewise
    for line in fromolLogFile.readlines():
        firstTwoChars = line[:2] # First 2 chars of line
        otherChars = line[2:] # Char 3 to end of line

        if firstTwoChars == '##':
            arr_new_lines.append(otherChars)
        elif firstTwoChars == "D:":
            arr_dates.append(otherChars)
        elif firstTwoChars == "C:":
            arr_commands.append(otherChars)
        elif firstTwoChars == "T:":
            arr_titles.append(otherChars)
        elif firstTwoChars == "P:":
            arr_pids.append(otherChars)
        else:
            print "+++++ Unexpected log content +++++"
            print " Please report at https://github.com/yafp/fromo/issues"

    fromolLogFile.close() # close the log file
    print "Finished reading log (arrays are filled)"


    ############################################################################
    # WRITING REPORT
    ############################################################################
    print "\nStarting HTML generation..."

    # Generate a timestamp
    date_string = u.get_timestamp()

    # define log document
    writepath = date_string+'.html'

    mode = 'a' if os.path.exists(writepath) else 'w' # append if logfile exists
    with open(writepath, mode) as f:
        f.write('<html>\n')
        # html head
        f.write('<head>\n')
        f.write('<title>fromo_analyzer report</title>\n')
        f.write('<script src="https://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>')
        f.write('<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">')
        f.write('<script type="text/javascript" src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>')
        f.write('<script>$( document ).ready(function() {$(\'#example\').DataTable({"lengthMenu": [[10, 50, 100,  -1], [10, 50, 100, "All"]]});});</script>')
        f.write('</head>\n')
        # html body
        f.write('<body>\n')
        f.write('<h1>fromo_analyzer report</h1>\n')
        f.write('<table id="example" class="display" cellspacing="0" width="100%">\n')
        f.write('<thead><tr><th>Timestamp</th><th>Command</th><th>Title</th><th>PID</th></tr></thead>\n')
        f.write('<tbody>\n')
        # prepare array iteration
        aD = iter(arr_dates)
        aC = iter(arr_commands)
        aT = iter(arr_titles)
        aP = iter(arr_pids)
        # loop over the arrays
        for x in range(0, len(arr_dates)):
            f.write('<tr><td>'+aD.next()+'</td><td>'+aC.next()+'</td><td>'+aT.next()+'</td><td>'+aP.next()+'</td></tr>\n')
        f.write('</tbody>\n')
        f.write('<tfoot><tr><th>Timestamp</th><th>Command</th><th>Title</th><th>PID</th></tr></tfoot>\n')
        f.write('</table>\n')
        f.write('<hr>\n')
        f.write('<p><small><center>Generated by <a href="https://github.com/yafp/fromo">fromo</a> at '+date_string+'</center></small></p>')
        f.write('</body>\n')
        f.write('</html>\n')
    f.close()
    print "Finished HTML generation"

else:
    puts(colored.red('[FAILED]')+'\tUnsupported operating system, aborting')
    sys.exit()
