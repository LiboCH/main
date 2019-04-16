#!/usr/bin/python3
import argparse
import xml.etree.ElementTree as ET
import pprint
from pathlib import Path

bankRelTemplate="""
<data>
    <bank>{ipid}</bank>
</data>
"""

def get_bank_relationship(p_ipid, p_argList):
    t_request = bankRelTemplate.replace('{ipid}',p_ipid)
    print(t_request)

def get_column_place(p_filename, p_colName, p_separator=';'):
    t_file = Path(p_filename)
    if t_file.is_file():
        with open(p_filename,'r') as file:
            t_header=file.readline().rstrip().split(p_separator)
        file.close()
        print(t_header)
        try:
            return t_header.index(p_colName)
        except:
            print("Unable to find column: {}". format(p_colName))
            return -1
    else:
        print ('File not found: {}'.format(p_filename))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cdcproxy', help = 'CDCProxy WS endpoint')
    parser.add_argument('infile', help = 'csv input file')
    parser.add_argument('ipid_col',metavar='ipid-col', help = 'column with ipid to be translated')
    args = parser.parse_args()
    pprint.pprint(args)
    t_ipidPos = get_column_place(args.infile, args.ipid_col)

    tree = ET.parse('response.xml')
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)
    
    get_bank_relationship('test','')

if __name__ == "__main__":
    main()

