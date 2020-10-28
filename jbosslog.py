#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import traceback
import sys


CLEAR =  '\033[0m'
RED = '\033[31m'
BOLD = '\033[1m'
WHITE = '\033[1;37m'
RED_BACKGROUND = '\033[1;41m'
JBOSS_DEFAULT_BOUNDARY = r"(20[12][0-9]-[01][0-9]-[0123][0-9] )?[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] [A-Z]+[\s]+\[.*\] \(.*\) .*"

class jbosslog:

    def __init__(self, stream=None, boundary=JBOSS_DEFAULT_BOUNDARY):
        """
        Open and instantiate jboss server.log.
        The first argument `stream` of the constructor is a stream.
        The second `boundary` is a boundary to separate log entries. It should be a python regex.
        If you do not specify `boundary`, the default boundary is used. It is suitable for default log format.
        If you use your own custom log format, you need to specify a python regex for a boundary.

        >>> log = jbosslog(stream="test/server.log")
        >>> print log.stream
        test/server.log
        >>> print log.boundary
        (201[0-9]-[01][0-9]-[0123][0-9] )?[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] [A-Z]+[\s]+\[.*\] \(.*\) .*
        >>> log.close()

        >>> log = jbosslog(stream="test/server.log", boundary=r"2015-01-05 .* test regex")
        >>> print log.stream
        test/server.log
        >>> print log.boundary
        2015-01-05 .* test regex
        >>> log.close()

        If stream or boundary is None, it throws an exception.

        >>> #log = jbosslog(stream=None, boundary=r"2015-01-05 .* test regex")
        """
        if stream == None:
            self._stream = sys_stdin_wrapper()
        else:
            self._stream = stream
        if boundary == None:
            raise Exception("jbossutils: boundary is None")
        #self._filename = open(filenname, 'r')
        self._position = self._stream.tell()
        self._lastread = self._stream.readline()
        self._boundary = boundary
        self._pattern = re.compile(self._boundary)
        
    @property
    def stream(self):
        return None

    @stream.getter
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream

    @property
    def boundary(self):
        return None

    @boundary.getter
    def boundary(self):
        return self._boundary

    @boundary.setter
    def boundary(self, boundary):
        self._boundary = boundary
        self._pattern = re.compile(boundary)

    def position(self):
        return self._position

    def seek(self, offset):
        self._stream.seek(offset,0)
        self._lastread = self._stream.readline()
        self._position = self._stream.tell()

    def match(self, line):
        if (line == None):
            return False
        matches = self._pattern.match(line)
        if (matches == None):
            return False
        else:
            return True

    def hasnext(self):
        if (self._lastread == ""):
            return False
        else:
            return True

    def next(self):
        self._position = self._stream.tell() # ここまで読んだ
        str=self._lastread
        #for line in self._stream: # using `for`, self._stream.tell() returns a wrong value
        while True:
            line = self._stream.readline()
            if line == "": # exit while loop when reaching EOF
                self._lastread = "" # reach EOF
                return jbosslogentry(str)
            if (self.match(line)): # if match boundary
                self._lastread = line
                return jbosslogentry(str)
            self._position = self._stream.tell() # ここまで読んだ
            str = str+line

    def close(self):
        self._stream.close()

class jbosslogentry:
    def __init__(self, string):
        """
        Instantiate a log entry.

        >>> import re
        >>> entry = jbosslogentry("16:44:20,591 DEBUG [org.jboss.as.config] (MSC service thread 1-7) xxx:\\n"
        ... + "awt.toolkit = sun.awt.X11.XToolkit\\n"
        ... )
        >>> entry.match(r"[\s]sun.")
        True
        >>> entry.match(r"hoge")
        False
        >>> entry.match(r".o.")
        True
        >>> print entry.highlight
        16:44:20,591 DEBUG \033[31m\033[1m[or\033[0mg.j\033[31m\033[1mbos\033[0ms.as.\033[31m\033[1mcon\033[0mfig] (MSC service thread 1-7) xxx:
        awt.\033[31m\033[1mtoo\033[0mlkit = sun.awt.X11.X\033[31m\033[1mToo\033[0mlkit
        <BLANKLINE>

        Since MULTILINE mode is enabled, you don't need '(?m)' in a regex. It is useful when you use it with '^' and '$'.

        >>> entry = jbosslogentry("16:44:20,591 DEBUG [org.jboss.as.config] (MSC service thread 1-7) xxx:\\n"
        ... + "awt.toolkit = sun.awt.X11.XToolkit\\n"
        ... )
        >>> entry.match(r"^awt")
        True
        >>> print entry.highlight
        16:44:20,591 DEBUG [org.jboss.as.config] (MSC service thread 1-7) xxx:
        \033[31m\033[1mawt\033[0m.toolkit = sun.awt.X11.XToolkit
        <BLANKLINE>
        """
        self._string = string
        self._highlight = None
        self._pattern = None

    @property
    def string(self):
        return None

    @string.getter
    def string(self):
        return self._string

    @property
    def highlight(self):
        return None

    @highlight.getter
    def highlight(self):
        if self._highlight != None:
            return self._highlight
        lastmatch = 0
        buf = ""
        for match in re.finditer(self._pattern, self._string):
            start, end = match.span()
            buf += self._string[lastmatch: start]
            buf += RED + BOLD
            buf += self._string[start: end]
            buf += CLEAR
            lastmatch = end
        buf += self._string[lastmatch:]
        self._highlight = buf
        return self._highlight

    def match(self, patternstr):
        self._highlight = None
        self._pattern = re.compile(patternstr, re.MULTILINE)
        #print "None? =" + str(self._string==None)
        match = self._pattern.search(self._string)
        if match != None:
            return True
        else:
            return False

class sys_stdin_wrapper:
    """Wrapper of stdin to fake up tell and seek methods"""
    def __init__(self):
        pass

    def readline(self):
        return sys.stdin.readline()
        
    def close( self ):
        pass

    def tell(self):
        return 0

    def seek(self, offset, whence):
        raise Exception('not supported')


# test code
if __name__ == '__main__':
    import doctest
    doctest.testmod()
