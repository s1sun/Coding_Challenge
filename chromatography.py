#!/usr/bin/env python3
# Author: Shaojun Sun

def canconcate_items(row, delim):
    # pre: given a list of string row and delimilator
    # post: return a string, each element canconcated by delimilator 
    mystr = ""
    if len(row) > 0:
        mystr = str(row[0])
    for i in range(1, len(row)):
        mystr += delim + str(row[i])
    return mystr

def write_to_csv(csv_file, title,  data, line_end='\n'): # over different platforms
    # pre: given csv_file pathway, a list of title, and 2D arrays
    # post: save to csv file without CR line break
    with open(csv_file, 'w', newline='') as f:
        str_title = canconcate_items(title, ',')
        f.write(str_title)
        for row in data:
            str_line = canconcate_items(row, ',')
            f.write( line_end + str_line )
