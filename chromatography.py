#!/usr/bin/env python3
# Author: Shaojun Sun
from decimal import Decimal, ROUND_HALF_EVEN

def precision_round(value, decimal, decimal_str):
    """
    Get a precise rounding behavior instead of round() function in python yielding un expected results. 

    Args:
        value (float): The value that needs to be rounded.
        decimal(int): The precision number to use for rounding
        decimal_str (str): Accuracy string with corresponding decimal, such as "0.0001' for 4 decimal.

    Returns:
        str: Concatenated string with elements separated by the delimiter.
    """
    value_str = str(value)
    number = Decimal(value_str)
    result = number.quantize(Decimal(decimal_str), rounding=ROUND_HALF_EVEN)
    return float(result)

def canconcate_items(row, delim):
    """
    Concatenates a list of string elements into a single string with a specified delimiter.

    Args:
        row (list of str): List of string elements to concatenate.
        delim (str): Delimiter to use between elements.

    Returns:
        str: Concatenated string with elements separated by the delimiter.
    """
    mystr = ""
    if len(row) > 0:
        mystr = str(row[0])
    for i in range(1, len(row)):
        mystr += delim + str(row[i])
    return mystr

def write_to_csv(csv_file, title,  data, line_end='\n'): # over different platforms
    """
    Writes a title and 2D array of data to a CSV file, with an optional parameter for line ending characters.

    Args:
        csv_file (str): Pathway of the CSV file to write to.
        title (list of str): List of title elements for the CSV.
        data (list of list of str): 2D array of data to write to the CSV.
        line_end (str, optional): Line ending character(s) for the CSV file. Defaults to '\n'.

    Returns:
        None
    """
    with open(csv_file, 'w', newline='') as f:
        str_title = canconcate_items(title, ',')
        f.write(str_title)
        for row in data:
            str_line = canconcate_items(row, ',')
            f.write( line_end + str_line )
