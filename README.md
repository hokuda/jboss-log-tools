* install

        $ git clone https://github.com/hokuda/jboss-log-tools.git
        $ cd jboss-log-tools
        $ git clone https://github.com/splunk/splunk-sdk-python.git

* start server

        $ su -
        # cd /usr/local/splunk/bin
        # ./splunk start

* run

        $ python search_mystudy.py "s" --output_mode=csv




-----------

# jboss-log-tools

Tools for analysing JBoss AS/EAP log files.

##jboss-log-grep

Usage:

        $ jboss-log-grep <pattern> <file>

Example:

        $ ./jboss-log-grep "hokuda.+hoge" server.log 
        16:46:08,856 TRACE [org.teiid.PROCESSOR] (Worker0_QueryProcessorQueue2) AccessNode(0) sending TupleBatch; beginning row=1, number of rows=4, lastBatch=1
                1: [hokuda, password, hoge, hoge, fuga]
                2: [user1, password, hoge, null, null]
                3: [user2, password, hoge, null, null]
                4: [user3, password, hoge, null, null]


##teiid-query-duration

Usage:

        $ teiid-query-duration <threshold> <file>

Example:

        [hokuda@localhost jboss-log-tools]$ ./teiid-query-duration 0 server.log 
        >>> duration in second = 0.047
        request ID = j5nPRpxMHbWt.0
        sql        = /*+ cache */ SELECT * FROM vvv.USERS
        start time = 2014-11-20 16:58:28.894000
        end time   = 2014-11-20 16:58:28.941000
        
        >>> duration in second = 0.046
        request ID = YOOIyAcSghcO.0
        sql        = /*+ cache */ SELECT * FROM vvv.USERS
        start time = 2014-11-20 17:01:28.363000
        end time   = 2014-11-20 17:01:28.409000

##teiid-extract-request

Usage:

        $ teiid-extract-request <reqid> <file>

Example:

        $ teiid-extract-request CYpbNi6727D+.0 server.log
        16:46:08,501 DEBUG [org.teiid.COMMAND_LOG] (New I/O worker #6) 	START USER COMMAND:	startTime=2014-11-20 16:46:08.501	requestID=CYpbNi6727D+.0	txID=null	sessionID=CYpbNi6727D+	applicationName=JDBC	principal=user@teiid-security	vdbName=test	vdbVersion=1	sql=SELECT * FROM vvv.USERS
        16:46:08,504 TRACE [org.teiid.PROCESSOR] (New I/O worker #6) after executeRequest : org.teiid.client.util.ResultsFuture@19e3c36c
        16:46:08,504 TRACE [org.teiid.RUNTIME] (Worker0_QueryProcessorQueue0) Beginning work with virtual worker Worker0_QueryProcessorQueue0
        (snip)
        16:46:08,937 DEBUG [org.teiid.COMMAND_LOG] (Worker0_QueryProcessorQueue3) 	END USER COMMAND:	endTime=2014-11-20 16:46:08.937	requestID=CYpbNi6727D+.0	txID=null	sessionID=CYpbNi6727D+	principal=user@teiid-security	vdbName=test	vdbVersion=1	finalRowCount=4


##Installation

Copy jboss-log-grep, jbosslogutils.py, teiid-extract-request, and teiid-query-duration to your bin directory.
