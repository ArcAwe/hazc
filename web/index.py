#!/usr/local/bin/python3

# enable debugging
import cgitb, sys, socket
cgitb.enable()

import xml.etree.cElementTree as ET

# OPTION 1: Read from XML files as it's own thread
tree = ET.parse('devices.xml')
root = tree.getRoot()

print("<table>")
print("<tr><td>Name</td><td>Description</td></tr>")
for device in root:
    print("<tr>")
    
    print("<td>" + device.tag + "</td>")
    
    print("<td>" + device.tag + "</td>")
    
    print("</tr>")
    
print("</table>")

