#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, urllib
import socket
import sys
from xml.etree import ElementTree
import httplib

#Replace following URL to appropriate URL 
url = 'http://localhost/cgi-bin/server.py'
query_args = {
    'lat'      : 34.87736,
    'lng'      : 138.52908,
    'radius'   : 10000.0,
    'from'     : 1,
    'to'       : 1,
    'format'   : 'xml',
    'placetype': 'city',
    'indent'   : 'true',
    }

data = urllib.urlencode(query_args)


def main():
    try:
        response = urllib2.urlopen(url, data, timeout=5)
        perf_data = ''
        tree = ''
        Qtime = ''
        # READ XML Response
        try:
           response_content = response.read(1024)
           tree = ElementTree.fromstring(response_content)
           for value in tree.getiterator(tag='QTime'):
               Qtime = value.text
           perf_data = "|Qtime=" + str(Qtime) + 'sec;;;;' 
        except httplib.IncompleteRead as e:
           # Just in case server responds IncompleteRead response
           tree = ElementTree.fromstring(e.partial)
           for value in tree.getiterator(tag='QTime'):
               Qtime = value.text
           perf_data = "|Qtime=" + str(Qtime) + 'sec;;;;'
        # Work on Response Code 
        response_code = response.getcode()
        if response_code == 200:
            print 'OK: Application is running fine' + perf_data
            sys.exit(0)
    except urllib2.URLError, e:
        #reason = e.reason
        #print 'CRITICAL: Application has issue: ' + str(reason)
        # TODO - reason should work, find out what's equivallent in old version
        print 'CRITICAL: Application has issue'
        sys.exit(2)


if __name__ == '__main__':
    main()
