#!/usr/bin/env python
"""
MagPy - Basic Runtime tests including durations  
"""
from __future__ import print_function

from magpy.stream import *   
from magpy.database import *   
import magpy.transfer as tr
import magpy.absolutes as di
import magpy.mpplot as mp
import magpy.opt.emd as emd
import magpy.opt.cred as cred

import os, getopt

def getfilenames(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
                #if file.endswith(".txt"):
                #print(os.path.join(root, file))
                filelist.append(os.path.join(root, file))
    return filelist

def loadtest(filename, fullheader=False):
    print (" ---------------------------------")
    print (" --------- READ TEST -------------")
    print (" ---------------------------------")
    try:
        t1 = datetime.utcnow()
        stream = read(filename,debug=fullheader)
    except:
        print ("Reading data {} failed".format(filename))
        return False
    if stream.length()[0] > 0:
        print ("Success for {}: {}".format(stream.header.get('DataFormat'),filename))
        print (" - lenght:          {}".format(stream.length()[0]))
        print (" - keys:            {}".format(stream._get_key_headers()))
        t2 = datetime.utcnow()
        print (" - load duration:   {}".format(t2-t1))
        print (" - SensorID:        {}".format(stream.header.get('SensorID',"!! not available !!")))
        if fullheader:
            print (" ------------------------------")
            print (" - Extended HEADER Information:")
            for dat in stream.header:
                print ("    -> Key: {}   --  Value: {}".format(dat, stream.header[dat]))
            print (" ------------------------------")
        return True
    else:
        return False

def writetest(source,destination,fmt):
    print (" ---------------------------------")
    print (" --------- WRITE TEST ------------")
    print (" ---------------------------------")
    stream = read(source)
    t1 = datetime.utcnow()
    print ("Writing format {}".format(fmt))
    if stream.write(destination,filenamebegins="mptest_",format_type=fmt):
        print("Writing successful for {} to {}".format(fmt,destination))
        t2 = datetime.utcnow()
        print (" - Needed {} sec for {} datapoints".format(t2-t1,stream.length()[0]))
        return True
    else:
        return False

def writeDBtest(db,source):
    print (" ---------------------------------")
    print (" -------- DB WRITE TEST ----------")
    print (" ---------------------------------")
    stream = read(source)
    t1 = datetime.utcnow()
    if stream.writeDB(db):
        print("Writing successful for {} to {}".format(fmt,destination))
        t2 = datetime.utcnow()
        print (" - Needed {} sec for {} datapoints".format(t2-t1,stream.length()[0]))
        return True
    else:
        return False

def main(argv):
    fmtlist = ''
    source = ''
    destination = ''
    path = ''
    database = ''
    intensive = False
    fmts = ['']
    for fmt in PYMAG_SUPPORTED_FORMATS:
        if 'w' in (PYMAG_SUPPORTED_FORMATS[fmt][0]):
            fmts.append(fmt)
    try:
        opts, args = getopt.getopt(argv,"hp:s:o:f:d:i",["path=","source=","destination=","fmtlist=","database=",])
    except getopt.GetoptError:
        print ('mptest.py -p <path> -s <source> -o <destination> -f <fmtlist> -d <database> -i <intensive>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('-------------------------------------')
            print ('Description:')
            print ('MagPy test programm for platform test')
            print ('-------------------------------------')
            print ('Usage:')
            print ('mptest.py -p <path> -s <source> -o <destination> -f <fmtlist> -d <database> -d <database>')
            print ('-------------------------------------')
            print ('Options:')
            print ('-p       : path for test data files')
            print ('-s       : single source file for write format tests')
            print ('-o       : output destination path')
            print ('-f       : list of formats to be checked (not yet available)')
            print ('-d       : name of a database for db type')
            print ('-i (-)   : intensive')
            print ('-------------------------------------')
            print ('Examples:')
            print ('python mptest.py -p mypath')
            print ('python mptest.py -p "/media/leon/237A-97B1/MagPyTest/TestFiles" -f IMAGCDF -s /media/leon/237A-97B1/MagPyTest/TestFiles/bsl20150113dsec.sec -o /tmp/')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-d", "--database"):
            database = arg
        elif opt in ("-o", "--destination"):
            destination = arg
        elif opt in ("-f", "--fmtlist"):
            fmtlist = arg
            try:
                fml= []
                fm = fmtlist.split(',')
                for el in fm:
                    if el in fmts:
                        fml.append(el)
                    else:
                        print (" - Selected format {} is not available for writing".format(el))
                fmts = [el for el in fml]
            except:
                print (" - error in option fmtlist - using default formats")
        elif opt in ("-i", "--intensive"):
            intensive = True

    fmts = [el for el in fmts if not el == '']

    # Summary info:
    failedload = []
    failedwrite = []

    if path == '' and source == '':
        print ('Specify a path and/or single data source:')
        print ('-- check mptest.py -h for more options and requirements')
        sys.exit()
    if not path == '':
        filelist = getfilenames(path)
        for f in filelist:
            val = loadtest(f, fullheader=intensive)
            if not val:
                failedload.append(f)
    if not destination == '' and not source == '':
        for fmt in fmts:
            val = writetest(source,destination,fmt)
            if not val:
                failedwrite.append(fmt)

    print ("\n----------------------------------")
    print ("-----------  SUMMARY  ------------")
    print ("----------------------------------")
    if not len(failedload) > 0 and not len(failedwrite) > 0:
        print ("\nALL TESTS SUCCESSFULLY PASSED!")
    else:
        print ("\nFailed to load (files):    {}".format(failedload)) 
        print ("\nFailed to write (formats): {}".format(failedwrite)) 

if __name__ == "__main__":
   main(sys.argv[1:])


