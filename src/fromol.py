#!/usr/bin/env python2
# coding=utf-8
# Name:			fromol.py
# Function:		logger - logs the frontmost window on Linux systems
# URL:          https://github.com/yafp/fromo
# Date:			20160602
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



####################################
# IMPORTS
####################################
import commands     # for checking for commands
import datetime     # for timestamp handling
import os           # to clear the screen & os detection
import subprocess   # for getting current apps & frontmost
import sys          # to exit & detect platform
import syslog       # to access syslog
import socket       # for getting current apps & frontmost
import threading    # for running a thread

from clint.textui import colored, puts  # for colored text

# unsure if really needed
#import signal # thread & escaping it


# to avaid issues with ASCII vs UTF 8 - i.e. with writing frontmostWindowTitle of Atom Editor into logfile
reload(sys)
sys.setdefaultencoding("utf-8")


####################################
# CONSTANT
####################################
version = 20160602.01


####################################
# CONFIG
####################################
# interval to check for current frontmost window
checkInterval = 5.0             # in seconds. Example: 10.0
# write log file or not
enableLogFileCreation = "false" # true or false. Only true results in a logfile


####################################
# CHECK REQUIREMENTS
####################################
def checkRequirementsOnStartup():

    if sys.platform == "linux" or sys.platform == "linux2": # check if platform is supported or not
        os.system('clear')  # # clear the screen
        print " __"
        print "/ _|"
        print "| |_ _ __ ___  _ __ ___   ___"
        print "|  _| '__/ _ \| '_ ` _ \ / _ \\"
        print "| | | | | (_) | | | | | | (_) |"
        print "|_| |_|  \___/|_| |_| |_|\___/      Version:"+str(version)+"\n"

        puts(colored.yellow('Checking requirements ...'))
        # test xprop (if status=0 =>ok && 512=not found )
        #status, result = subprocess.getstatusoutput("ls /usr/bin/xprop") # python3
        status, result = commands.getstatusoutput("ls /usr/bin/xprop") # python2
        if status == 512: #not found
            puts(colored.red('[FAILED]')+'\tUnable to find xprop, aborting.')
            sys.exit()
        else: #found
            puts(colored.green('[  OK  ]')+'\tFound xprop')

        # test wmctrl
        status, result = commands.getstatusoutput("ls /usr/bin/wmctrl") # python2
        if status == 512: # not found
            puts(colored.red('[FAILED]')+'\tUnable to find wmctrl, aborting.')
            sys.exit()
        else: #found
            puts(colored.green('[  OK  ]')+'\tFound wmctrl\n')
    else: # not on linux - quit the script
        puts(colored.red('[FAILED]')+'\tUnsupported operating system, aborting')
        sys.exit()


####################################
# GENERATE AND RETURN A TIMESTAMP AS STRING
####################################
def getTimestamp():
    d = datetime.datetime.now()
    dateString = str(d)
    puts(colored.yellow("~~~ "+dateString+" ~~~"))
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
    print "Command:\t"+frontmostCommand
    print "Title:\t\t"+frontmostWindowTitle
    print "PID:\t\t"+frontmostWindowPID
    print ""

    return (frontmostCommand, frontmostWindowTitle, frontmostWindowPID)


####################################
# RUN THREAD ALL x SECONDS
####################################
def fromoLogger():
    #try:
    #puts(colored.yellow('Gathering frontmost window'))
    threading.Timer(checkInterval, fromoLogger).start()

    dateString = getTimestamp() # get timestamp
    frontmostCommand, frontmostWindowTitle, frontmostWindowPID = getFrontmostWindowData() # get data about current frontmost window

    # write to log-file
    if enableLogFileCreation == "true":
        with open("fromol.log", "a") as fromolLogFile:
        #with open("/var/log/fromo/fromol.log", "a") as myfile:
            #myfile.write(dateString+'\t'+frontmostCommand+'\t'+frontmostWindowTitle+'\n')
            fromolLogFile.write(dateString+'\n'+frontmostCommand+'\n'+frontmostWindowTitle+'\n'+frontmostWindowPID+'\n###\n')

    #signal.pause() # instead of: while True: time.sleep(100)
    #except (KeyboardInterrupt):
    #print '\n! Received keyboard interrupt, quitting threads.\n'
    #sys.exit()


###############################################################################
# MAIN
###############################################################################

# check requirements on startup
checkRequirementsOnStartup()

# display config values on startup
puts(colored.yellow('Configuration'))
print "Interval (sec):\t"+str(checkInterval)
print "LogFile:\t"+enableLogFileCreation

# Notify logger-startup to syslog
#
# on Fedora: /var/log/messages
# on Ubuntu: /var/log/syslog
#
#syslog.syslog("FROMO - Starting the fromo logger now")
syslog.syslog(syslog.LOG_INFO, "FROMO - Starting the fromo logger now") # INFO priority

# start logger-core
puts(colored.yellow('\nStarting fromo logger now\n'))
fromoLogger()
