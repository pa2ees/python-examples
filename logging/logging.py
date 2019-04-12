import logging

log_level = logging.DEBUG

logging.basicConfig(level=log_level, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)

log.debug("logging level: {}".format(log.level))


------------------------------------------------------

# LOGGING TO CONSOLE WITH COMMAND LINE SWITCHES
import logging
import os
import getopt

TRACKER_LOG_VIEWER_VERSION = "1.3.1"

log_level = logging.ERROR
LOG_LEVEL_OPTIONS = ['debug', 'info', 'warning', 'error', 'fatal']

def usage():
    print "python {} [-l <level>]\n".format(os.sys.argv[0])
    print "log levels: {}".format(', '.join(LOG_LEVEL_OPTIONS))


try:
    opts, args = getopt.getopt(os.sys.argv[1:], "l:",[])
except getopt.GetoptError:
    usage()
    os.sys.exit(2)

for opt, arg in opts:
    if opt == "-l":
        if arg in LOG_LEVEL_OPTIONS:
            log_level = (LOG_LEVEL_OPTIONS.index(arg) + 1) * 10

logging.basicConfig(level=log_level, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)
log.level = log.getEffectiveLevel()

log.debug("logging level: {}".format(log.level))

------------------------------------------------------

# LOGGING TO CONSOLE AND FILE WITH COMMAND LINE SWITCHES
import logging, os, getopt

BIT_VERSION = "2.0"

log_level = logging.INFO
LOG_LEVEL_OPTIONS = ['debug', 'info', 'warning', 'error', 'fatal']

def usage():
    print("python3 {} [-l <level>]\n".format(os.sys.argv[0]))
    print("log levels: {}".format(', '.join(LOG_LEVEL_OPTIONS)))


try:
    opts, args = getopt.getopt(os.sys.argv[1:], "l:f:",[])
except getopt.GetoptError:
    usage()
    os.sys.exit(2)

log_fname = None

for opt, arg in opts:
    if opt == "-l":
        if arg in LOG_LEVEL_OPTIONS:
            log_level = (LOG_LEVEL_OPTIONS.index(arg) + 1) * 10
    if opt == "-f":
        log_fname = arg
        
logging_formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(logging_formatter)

#logging.basicConfig(level=log_level, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)
log.level = log_level
log.addHandler(logging_handler)

if log_fname != None:
    logging_file_handler = logging.FileHandler(log_fname)
    logging_file_handler.setFormatter(logging_formatter)
    log.addHandler(logging_file_handler)
