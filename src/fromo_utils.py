#!/usr/bin/env python2
# coding=utf-8
# Name:			fromo_utils.py
# Function:		contains utils used in both components
# URL:          https://github.com/yafp/fromo
# Author: 		https://github.com/yafp/
#               http://yafp.de
#

""" fromo_utils - Utils for the fromo project """

################################################################################
# IMPORTS
################################################################################
import datetime     # for timestamp handling


################################################################################
# GENERATE AND RETURN A TIMESTAMP AS STRING
################################################################################
def get_timestamp():
    """ generate and return a timestamp """
    date_time_object = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_string = str(date_time_object)
    return date_string
