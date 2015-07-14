#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./splunk-sdk-python"))
from splunklib.binding import HTTPError
import splunklib.client as client
from utils import *

# hokuda
#from splunklib.results import *

class splunkstream:
    """Input stream of Splunk log. Supports readline, tell, and seek methods"""
    def __init__(self):
        search = 'search * | sort _time'
        service = client.connect(username='admin', password='password', host='localhost', port='8089')
        job = service.jobs.create(search)
        while True:
            while not job.is_ready():
                pass
            if job['isDone'] == '1': 
                break
        self._job = job
        from splunklib.results import ResultsReader
        self._reader = ResultsReader(job.results())
        self._buffer = self._reader.next()['_raw']
        self._stringio = StringIO.StringIO(self._buffer)

    def readline(self):
        line = self._stringio.readline()
        if line == '':
            try:
                self._buffer = self._reader.next()['_raw']
            except StopIteration:
                return ''
            self._stringio = StringIO.StringIO(self._buffer)
            line = self._stringio.readline()
        if not line.endswith('\n'):
            line = line + '\n'
        #print line,
        return line
        
    def close( self ):
        self._job.cancel()

    def tell(self):
        return 0

    def seek(self, offset, whence):
        raise Exception('not supported')

        
if __name__ == "__main__":
    stream = splunkstream()
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),
    print stream.readline(),

