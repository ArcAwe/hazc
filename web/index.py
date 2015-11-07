#!/usr/local/bin/python3

# enable debugging
import cgitb, sys, socket
cgitb.enable()

# OPTION 1: Read from XML file


# OPTION 2: Really this is redirecting/interpreting web calls, so that it is more extensible and is easier to install

socket.socket(socket.AF_INET, socket.SOCK_STREAM)