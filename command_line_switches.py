import getopt, os, logging

log_level = logging.INFO

LOG_LEVEL_OPTIONS = ['debug', 'info', 'warning', 'error', 'fatal']


def usage():
    usage_strings = [{"switch": "-l", "parameter":"<level>", "separator":":", "description":"changes the logging level"},
                     {"switch": "", "parameter":"", "separator":"", "description":"log levels: {}".format(', '.join(LOG_LEVEL_OPTIONS))},
                     {"switch": "-p", "parameter":"<page_name>", "separator":":", "description":"specify the page name"},
                     {"switch": "-s", "parameter":"<space_name>", "separator":":", "description":"specify the space name"}]

    p_width = 7
    for usage_string in usage_strings:
        if len(usage_string['parameter']) > p_width:
            p_width = len(usage_string['parameter'])
                     
    print("Switches:")
    for usage_string in usage_strings:
        usage_string['p_width'] = p_width
        print("{switch:>5} {parameter:{p_width}} {separator:1} {description}".format(**usage_string))

try:
    opts, args = getopt.getopt(os.sys.argv[1:], "hspf:o:l:v:r:",[])
except getopt.GetoptError:
    usage()
    os.sys.exit(2)

for opt, arg in opts:
    if opt == "-l":
        if arg in LOG_LEVEL_OPTIONS:
            log_level = (LOG_LEVEL_OPTIONS.index(arg) + 1) * 10
    if opt == "-h":
        usage()
        os.sys.exit(2)

        
log_level = logging.DEBUG
logging.basicConfig(level=log_level, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)

log.debug("logging level: {}".format(log.getEffectiveLevel()))

