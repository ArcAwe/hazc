#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, sys
cgitb.enable()

print("Content-Type: text/plain;charset=utf-8")
print()
print("Hello World!")
if(sys.version[0:1] != "3"):
    print("ERROR!!! Please alter your configuration to run python3!")
else:
    print("Success! Running at least Python 3")
print("\nPython version " + sys.version)
