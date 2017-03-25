#!/usr/bin/python

import sys
import getopt
import os
import re
import csv


class ReadLog(object):
    def __init__(self, input_file):
        self.ifile = input_file
        
    def __iter__(self):
        with open(self.ifile, "rb") as f:
            for line in f:
                yield to_unicode(line)


def to_unicode(byte_line):
    if isinstance(byte_line, str):
        value = byte_line.decode('utf-8')
    else:
        value = byte_line
    return value


def to_str(uni_line):
    if isinstance(uni_line, unicode):
        value = uni_line.encode('utf-8')
    else:
        value = uni_line
    return value


def extr_args(argv):
    arg_dict = {'inputfile' : [],
                'outputfile' : ''}
    if len(argv) < 4:
        print 'not enough arguments, 4 expected, try:'
        print 'logreader.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    
    iswitch = False
    for i, arg in enumerate(argv):
        if iswitch and arg != '-o':
            arg_dict['inputfile'].append(arg)
        elif arg == '-i':
            iswitch = True
        elif arg == '-o':
            iswitch = False
            arg_dict['outputfile'] = argv[i + 1]
    
    if len(arg_dict['inputfile']) == 0 or arg_dict['outputfile'] == '':
        print 'invalid arguments provided, try:'
        print 'logreader.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    
    return arg_dict


def extr_data(input_file, output_file):
    file_to_read = ReadLog(input_file)
    datapoints = ['date','time','sr','phone','member']
    file_to_write = open(output_file, 'ab')
    csv_writer = csv.DictWriter(file_to_write, datapoints, restval='',
                               extrasaction='ignore', dialect='excel')
    #csv_writer.writeheader()
    
    regex_code = re.compile(r'(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}).*'
                     r'SR Number: (?P<sr>[0-9]-[0-9]+)\s+'
                     r'Contact Number:(?P<phone>[0-9]{9,14}).*'
                     r'Member:(?P<member>.+$)', re.I)
    
    date = re.search(r'2017[0-9]{4}', input_file).group(0)
    
    for line in file_to_read:
        matches = regex_code.search(line)
        # the regex fails if even only one pattern doesn't match
        if matches is None:
            continue
        recd_dict = matches.groupdict()
        recd_dict['date'] = date
        csv_writer.writerow(recd_dict)
        
    file_to_write.close()
         
    
def main():
    arg_dict = extr_args(sys.argv[1:])
    input_list = arg_dict['inputfile']
    output = arg_dict['outputfile']
    
    for input_file in input_list:
        if os.path.isfile(input_file):
            extr_data(input_file, output)
        else:
            print 'invalid inputfile provided:'
            print input_file
            sys.exit(2)
        
    

if __name__ == "__main__":
   main()
   
