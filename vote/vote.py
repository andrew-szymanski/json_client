#!/usr/bin/env python

__author__ = "Andrew Szymanski ()"
__version__ = "0.1.0"

"""Post vote test harness
"""
import sys
import logging
import simplejson as json
import urllib    
import urllib2
import socket
import time
import os
import inspect

LOG_INDENT = "   "
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s',"%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger(__name__).addHandler(console)
logger = logging.getLogger(__name__)


class Publisher(object):
    """ Main class which does the whole workflow
    """
    def __init__(self, *args, **kwargs):
        """Create an object and attach or initialize logger
        """
        self.logger = kwargs.get('logger',None)
        if ( self.logger is None ):
            # Get an instance of a logger
            self.logger = logger
        # initial log entry
        log_level = kwargs.get('log_level', logging.DEBUG)
        self.logger.setLevel(log_level)
        self.logger.debug("%s: %s version [%s]" % (self.__class__.__name__, __file__,__version__))
        
        # initialize all vars to avoid "undeclared"
        # and to have a nice neat list of all member vars
        self.api_url = None
        


    def configure(self, *args, **kwargs):
        """ Grab and validate all input params
        Will return True if successful, False if critical validation failed
        """
        self.logger.debug("%s::%s starting..." %  (self.__class__.__name__ , inspect.stack()[0][3]))             

        # urls
        self.api_url = kwargs.get('api_url',None)     
        if not self.api_url:
            raise "api_url not specified"
            return False

        self.logger.debug("api_url: [%s]" % self.api_url)
        return True



    def publish_json(self, json_str):
        """ publish json
        """
        self.logger.debug("%s::%s starting..." %  (self.__class__.__name__ , inspect.stack()[0][3])) 
        
        # basic validation
        if ( not json_str or len(json_str) < 1):
             raise Exception("supplied json string empty")

        # grab all params needed
        url = self.api_url
        self.logger.debug("url: [%s]" % url)
        if ( not url or len(url) < 1 ):
            raise Exception("API url not defined: [%s]" % url)
        

        data = json_str
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        
        # post json data
        logger.info("posting json data [%s] to [%s]" % (data, url) )
        try:
            self.logger.debug("sending request...")
            f = urllib2.urlopen(req)
            self.logger.debug("reading response...")
            response = f.read()
            self.logger.debug("closing connection...")
            f.close()   
        except urllib2.HTTPError, e:
            return_message = "%s (%s)" % (e.read(), e)
            raise Exception(return_message)
        except urllib2.URLError, e:
            return_message = "%s %s" % (return_message, e)
            raise Exception(return_message)
        except Exception, e:
            return_message = "%s %s" % (return_message, e)
            raise Exception(return_message)
        logger.info("posting json data to server OK")
            
        # and return
        self.logger.debug("%s::%s DONE" %  (self.__class__.__name__ , inspect.stack()[0][3])) 
        return (return_status, return_message)

    
def send_json(*args, **kwargs):
    """ Send json to server
    """
    logger = kwargs.get('logger',None)
    json_file = kwargs.get('json_file',None)
    api_url = kwargs.get('api_url',None)

    logger.debug("send_json to [%s] starting, json_file=[%s]" % (api_url, json_file)) 
    
    json_str = ""
    # try to read json into a string
    try:
        with open(json_file) as f: 
            json_str = f.read()
    except IOError as e:
        self.logger.error("json_file could not be read: [%s], exception: [%s]" % (json_file, e) )
        return False
    logger.debug("json_str=[%s]" % json_str) 
    
    
    json_publisher = Publisher(logger=logger, log_level=logger.getEffectiveLevel())
    logger.debug("setting up publisher...") 
    result = json_publisher.configure(api_url=api_url)
    if not result:
        logger.error("Could not configure tracking publisher, some critical params invalid / missing.  See erors above.")
        sys.exit(1)
        
    logger.debug("setting up publisher DONE") 
    json_publisher.publish_json(json_str=json_str)
    
    


#                      **********************************************************
#                      **** mainRun - parse args and decide what to do
#                      **********************************************************
def mainRun(opts, parser):
    # set log level - we might control it by some option in the future
    if ( opts.debug != None ):
        logger.setLevel("DEBUG")
        logger.debug("logging level activated: [DEBUG]")
    logger.debug("number of input args: [" + str(len(sys.argv)-1) + "]")
    

    # check for json file param
    json_file = opts.json_file
    if not json_file:
        logger.error("json file not specified")
        parser.print_help()
        sys.exit(1)
        
    # check for api_url param
    api_url = opts.api_url
    if not api_url:
        logger.error("api_url not specified")
        parser.print_help()
        sys.exit(1)

    # run main method (which is also an example of using this module as a library)
    send_json(logger=logger,json_file=json_file,api_url=api_url)
        
        


# manual testing min setup:

# tested / use cases:
# ./vote.py
# ./vote.py  --debug=Y
# ./post_tracking_events.py --debug=Y --api_url=http://hostaname/api/...  --json_file=./tracking_data_sample.json


def main(argv=None):
    from optparse import OptionParser, OptionGroup
    logger.debug("main starting...")

    argv = argv or sys.argv
    parser = OptionParser(description="Vote test harness",
                      version=__version__,
                      usage="usage: %prog [options]")
    # cat options
    cat_options = OptionGroup(parser, "options")
    cat_options.add_option("--debug", help="debug logging, specify any value to enable debug, omit this param to disable, example: --debug=yes", default=None)
    cat_options.add_option("--api_url", help="full API url, example: --api_url=http://xxxxxx.appspot.com/api/v1.0/vote", default=None)
    cat_options.add_option("--json_file", help="json file containing metrics, example: --json_file=./sample.json", default=None)
    cat_options.add_option("--dry_run", help="if set (to anything), will go through the motions but will not post anything to server, example: --dry_run=Y", default=None)
    parser.add_option_group(cat_options)

    try: 
        opts, args = parser.parse_args(argv[1:])
    except Exception, e:
        sys.exit("ERROR: [%s]" % e)

    try:
        mainRun(opts, parser)
    except Exception, e:
        sys.exit("ERROR: [%s]" % e)


if __name__ == "__main__":
    logger.info("__main__ starting...")
    try:
        main()
    except Exception, e:
        sys.exit("ERROR: [%s]" % e)    
    
    
    
    
    