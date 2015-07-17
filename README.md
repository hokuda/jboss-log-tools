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

A command utility for grepping jboss server.log

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

A command line utility for timing user command query and data source comand query

Usage:

        teiid-query-duration [-h] [--threshold <sec>] [--src-command]
                            [--splunk | --local <file>]

Optional arguments:

        -h, --help            show this help message and exit
        --threshold <sec>, -t <sec>
                              Threshold of duration to be shown in second.
        --src-command, -s     Show src command duration.
        --splunk              Use splunk to feed log.
        --local-file <file>, -f <file>
                              Feed local log file. If neither --local-file and
                              --splunk is not specified, teiid-query-duration feeds
                              log from stdin.


Example:

        [hokuda@localhost jboss-log-tools]$ ./teiid-query-duration --threshold 0 --local server.log 
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

A command utility for extracting log messages for a specific request command

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

1. git clone this repo.

        git clone https://github.com/hokuda/jboss-log-tools.git

2. change directory.

        cd jboss-log-tools

3. (optional) git clone Splunk SDK.

        git clone https://github.com/splunk/splunk-sdk-python.git

4. copy the files to your bin directory

        cp -r * /path/to/your/bin/


###Splunk integration

The [teiid-query-duration](#teiid-query-duration) command can feed log stored in Splunk server. To enable Splunk integration feature, you need:

1. Install Splunk SDK (See [Installation](#installation))

2. Create ~/.splunkrc referring [this](https://github.com/splunk/splunk-sdk-python#splunkrc)