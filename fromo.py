#!/usr/bin/env python2
# coding=utf-8
# Name:			fromo.py
# Function:		Output the name of the FROntMOst window
# Date:			20160601
# Author: 		yafp
#               http://askubuntu.com/questions/555201/get-window-title-or-application-name-with-python
#
#
# Todo:
# - Check termcolor package
# - add log analyzer
# - optimize threading keyboardInterrupt:
#       http://stackoverflow.com/questions/3788208/python-threading-ignores-keyboardinterrupt-exception#3788243
#       http://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown



####################################
# IMPORTS
####################################
import threading    # for running a thread
import datetime     # for timestamp handling
import subprocess   # for getting current apps & frontmost
import socket       # for getting current apps & frontmost
import commands     # for checking for commands
import sys          # to exit
import os           # to clear the screen & os detection
import syslog       # to access syslog

from clint.textui import colored, puts  # for colored text
from sys import platform as _platform # for os & platform detection

import signal


####################################
# CONSTANT
####################################
version = 20160601.01


####################################
# CONFIG
####################################
#
# interval to check for current frontmost window
checkInterval = 5.0 # Example: 10.0


####################################
# CHECK REQUIREMENTS
####################################
def checkRequirementsOnStartup():
    # clear the screen
    if _platform == "linux" or _platform == "linux2" or platform == "darwin":
       os.system('clear')  # on linux / os x
    elif _platform == "win32":
       os.system('cls')  # on windows

    puts(colored.yellow('Checking requirements ...\n'))

    # test xprop (if status=0 =>ok && 512=not found )
    #status, result = subprocess.getstatusoutput("ls /usr/bin/xprop") # python3
    status, result = commands.getstatusoutput("ls /usr/bin/xprop") # python2
    if status == 512:
        print "[ERROR]\txprop is missing - aborting"
        sys.exit()
    else:
        print "[OK]\tFound xprop"

    # test wmctrl (if status=0 =>ok && 512=not found )
    status, result = commands.getstatusoutput("ls /usr/bin/wmctrl") # python2
    if status == 512:
        print "[ERROR]\twmctrl is missing - aborting"
        sys.exit()
    else:
        print "[OK]\tFound wmctrl\n"


####################################
# GENERATE AND RETURN A TIMESTAMP AS STRING
####################################
def getTimestamp():
    d = datetime.datetime.now()
    #print d.isoformat('T')
    dateString = str(d)
    print "Timestamp:\t"+dateString
    return dateString


####################################
# GET DATA OF FRONTMOST WINDOW
####################################
def getFrontmostWindowData():
    #1
    command = "xprop -root _NET_ACTIVE_WINDOW"
    output = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    frontmost = output.communicate()[0].decode("utf-8").strip().split()[-1]

    # 2
    fixed_id = frontmost[:2]+"0"+frontmost[2:]
    command = "wmctrl -lp"
    output = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    frontmostWindowPID = [l.split()[2] for l in output.communicate()[0].decode("utf-8").splitlines() if fixed_id in l][0]

    # 3
    command = "wmctrl -lp"
    output = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    window_list = output.communicate()[0].decode("utf-8")
    frontmostWindowTitle = [l for l in window_list.split("\n") if fixed_id in l][0].split(socket.gethostname()+" ")[-1]

    # MY MESS - GETTING PROCESS NAME from PID
    # http://stackoverflow.com/questions/4408377/how-can-i-get-terminal-output-in-python#4408409
    frontmostCommand = commands.getstatusoutput('cat "/proc/'+frontmostWindowPID+'/cmdline"')
    frontmostCommand = frontmostCommand[1]

    # output
    print "PID:\t\t"+frontmostWindowPID
    print "Command:\t"+frontmostCommand
    print "Title:\t\t"+frontmostWindowTitle
    print ""

    return (frontmostCommand, frontmostWindowTitle)


####################################
# RUN THREAD ALL x SECONDS
####################################
def loopMe():
    #try:
    puts(colored.yellow('Gathering frontmost window'))
    threading.Timer(checkInterval, loopMe).start()

    dateString = getTimestamp() # get timestamp
    frontmostCommand, frontmostWindowTitle = getFrontmostWindowData() # get data about current frontmost window

    # write to log-file
    with open("fromo.log", "a") as myfile:
        myfile.write(dateString+'\t'+frontmostCommand+'\t'+frontmostWindowTitle+'\n')

    #signal.pause() # instead of: while True: time.sleep(100)
    #except (KeyboardInterrupt):
    #print '\n! Received keyboard interrupt, quitting threads.\n'
    #sys.exit()


###############################################################################
# MAIN
###############################################################################
checkRequirementsOnStartup()

# on Fedora: /var/log/messages
syslog.syslog("FROMO - Starting the fromo logger now")
syslog.syslog(syslog.LOG_INFO, "FROMO - Test message at INFO priority")

print "Starting core app...\n"
loopMe()
