#!/usr/local/bin/python3

import xml.etree.ElementTree as ET

tree = ET.parse('devices.xml')

root = tree.getroot()

table = root.find("inftable")
version = table.find("version")
print("v: " + version.text)
controls = table.find("control")
for c in controls:
    print(c.tag)
    for attr in c:
        print("\t" + attr.tag + " " + attr.text)
        
new = ET.SubElement(root, 'new')
version = ET.SubElement(new, 'version')
version.text = "1.0"

tree.write('devices2.xml')

# for subtree in root:
#     print(subtree.tag)
#     for child in subtree:
#         print("\t" + child.tag + " " + child.text)
#         for child1 in child:
#             print("\t\t" + child1.tag + " " + child1.text)
#             for child2 in child1:
#                 print("\t\t\t" + child2.tag + " " + child2.text)