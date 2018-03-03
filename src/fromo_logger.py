#!/usr/bin/env python2
# coding=utf-8
# Name:			fromo_logger.py
# Function:		logger - logs the frontmost window on Linux systems
# URL:          https://github.com/yafp/fromo
# Author: 		https://github.com/yafp/
#               http://yafp.de
#
# Resources:
# -  Getting Window Title: http://askubuntu.com/questions/555201/get-window-title-or-application-name-with-python
#
# Todo:
# - setup some kind of log-rotation (using: logrotate?)
# - optimize threading keyboardInterrupt:
#       http://stackoverflow.com/questions/3788208/python-threading-ignores-keyboardinterrupt-exception#3788243
#       http://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown

""" fromo_logger - The fromo logging component """

################################################################################
# IMPORTS
################################################################################
import commands     # for checking for commands
import os           # to clear the screen & os detection
import subprocess   # for getting current apps & frontmost
import sys          # to exit & detect platform
import syslog       # to access syslog
import threading    # for running a thread
import argparse     # for parsing arguments
from clint.textui import colored, puts  # for colored text
# fromo imports
import fromo_utils as u
import fromo_constants as c


################################################################################
# CONFIG
################################################################################
ENABLELOGFILECREATION = True # true or false. Only true results in a logfile
VERBOSE = False # can be overwritten by argument


################################################################################
# CHECK REQUIREMENTS
################################################################################
def check_requirements_on_startup(VERBOSE):
    """ Check the script requirements """

    if sys.platform == "linux" or sys.platform == "linux2": # check if platform is supported or not
        os.system('clear')  # # clear the screen
        if VERBOSE:
            print " ___                   __"
            print "|  _|___ ___ _____ ___|  |"
            print "|  _|  _| . |     | . |  |__"
            print "|_| |_| |___|_|_|_|___|_____|    Version:"+str(c.VERSION)+"\n"

            puts(colored.yellow('Checking requirements ...'))

        # test xdotool
        status, result = commands.getstatusoutput("ls /usr/bin/xdotool") # python2
        if status == 512: # not found
            puts(colored.red('[FAILED]')+'\tUnable to find xdotool, aborting.')
            sys.exit()
        else: #found
            if VERBOSE:
                puts(colored.green('[  OK  ]')+'\tFound xdotool\n')

        if VERBOSE:
            # display config values on startup
            puts(colored.yellow('Configuration ...'))
            print "Interval (sec):\t"+str(CHECK_INTERVAL)
            print "LogFile:\t"+str(ENABLELOGFILECREATION)
            print "Verbose:\t"+str(VERBOSE)
    else: # not on linux - quit the script
        puts(colored.red('[FAILED]')+'\tUnsupported operating system, aborting')
        sys.exit()


################################################################################
# GET DATA OF FRONTMOST WINDOW
################################################################################
def get_frontmost_window_data(VERBOSE):
    """ get and return the current frontmost application name, pid and command """
    # get window name or title
    command = "xdotool getwindowfocus getwindowname"
    output = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    frontmostWindowTitle = output.communicate()[0].decode("utf-8").strip().split()[-1]

    # get window pid
    command = "xdotool getwindowfocus getwindowpid"
    output = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    frontmostWindowPID = output.communicate()[0].decode("utf-8").strip().split()[-1]

    # get command
    command = "cat /proc/"+str(frontmostWindowPID)+"/cmdline"
    output = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    frontmostCommand = output.communicate()[0].decode("utf-8").strip().split()[-1]

    # get  & print timestamp
    date_string = u.get_timestamp()

    if VERBOSE:
        puts(colored.yellow("~~~ "+date_string+" ~~~"))
        print "Title:\t\t"+frontmostWindowTitle
        print "PID:\t\t"+frontmostWindowPID
        print "Command:\t"+frontmostCommand

    return (frontmostCommand, frontmostWindowTitle, frontmostWindowPID)


################################################################################
# RUN THREAD ALL x SECONDS
################################################################################
def fromo_logger():
    """ the actual logging thread  & log file writer"""
    threading.Timer(CHECK_INTERVAL, fromo_logger).start()

    # get timestamp
    date_string = u.get_timestamp()

    # get data about current frontmost window
    frontmostCommand, frontmostWindowTitle, frontmostWindowPID = get_frontmost_window_data(VERBOSE)

    # write to log-file
    if ENABLELOGFILECREATION == True:
        with open("fromo.log", "a") as fromolLogFile:
            fromolLogFile.write('D:'+date_string+'\nC:'+frontmostCommand+'\nT:'+frontmostWindowTitle+'\nP:'+frontmostWindowPID+'\n##\n')


################################################################################
# MAIN
################################################################################

# handling arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--time", help="Defines logging interval in seconds")
parser.add_argument("-v", "--verbose", help="Write output to terminal", action='store_true')
args = parser.parse_args()

if args.time:
    CHECK_INTERVAL = float(args.time)
else:
    CHECK_INTERVAL = 3.0 # in seconds (float)

if args.verbose:
    VERBOSE = True

# check requirements on startup
check_requirements_on_startup(VERBOSE)

# Notify logger-startup to syslogv (INFO priority)
#
# on Fedora: /var/log/messages
# on Ubuntu: /var/log/syslog
syslog.syslog(syslog.LOG_INFO, "FROMO - Starting the fromo logger now")

# start logger-core
puts(colored.yellow('\nStarted fromo logger ...\n'))
fromo_logger()
