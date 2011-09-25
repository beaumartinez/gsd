import codecs
import os.path
import re
import sys

ENCODING = 'utf-8'

GSD_BLOCK_START = u'# GSD start'
GSD_BLOCK_END = u'# GSD end'

HOSTS_FILE_PATH = '/etc/hosts'

RAW_SITES_FILE_PATH = '~/.gsd-sites'
SITES_FILE_PATH = os.path.expanduser(RAW_SITES_FILE_PATH)

def read_sites_file(path, encoding=ENCODING):
    with codecs.open(path, encoding=encoding) as file_:
        contents = file_.read()

    sites = re.split('\s+', contents)

    # Remove duplicate and empty strings
    sites = frozenset(sites)
    sites = filter(lambda x: x != '', sites)

    sites = frozenset(sites)

    return sites

def get_gsd_block_position(path, encoding=ENCODING):
    with codecs.open(path, encoding=encoding) as file_:
        contents = file_.read()

    start = contents.index(GSD_BLOCK_START)
    end = contents.index(GSD_BLOCK_END)

    end += len(GSD_BLOCK_END)

    return start, end

def check_doesnt_have_gsd_block(path):
    try:
        get_gsd_block_position(path)
    except ValueError:
        pass
    else:
        raise ValueError('{} has a GSD block'.format(HOSTS_FILE_PATH))

def change_hosts_file(sites):
    check_doesnt_have_gsd_block(HOSTS_FILE_PATH)

    sites = sorted(sites)
    formatted_sites = (u'127.0.0.1 {}'.format(site) for site in sites)
    formatted_sites = u'\n'.join(formatted_sites)

    with codecs.open(HOSTS_FILE_PATH, encoding=ENCODING,
            mode='a') as hosts_file:
        hosts_file.write(GSD_BLOCK_START)
        hosts_file.write(u'\n')

        hosts_file.write(formatted_sites)
        hosts_file.write(u'\n')

        hosts_file.write(GSD_BLOCK_END)
        hosts_file.write(u'\n')

def restore_hosts_file():
    start, end = get_gsd_block_position(HOSTS_FILE_PATH)

    # Remove the EOL
    end += 1

    with codecs.open(HOSTS_FILE_PATH, encoding=ENCODING) as hosts_file:
        hosts_file_contents = hosts_file.read() 

    hosts_file_contents = (hosts_file_contents[:start] +
        hosts_file_contents[end:])

    with codecs.open(HOSTS_FILE_PATH, encoding=ENCODING,
            mode='w') as hosts_file:
        hosts_file.write(hosts_file_contents)

# Script

CANT_CHANGE_HOSTS_FILE_MESSAGE = ('Error: Can\'t change hosts file. Are you '
    'root?')

def start_getting_shit_done():
    try:
        sites = read_sites_file(SITES_FILE_PATH)
    except IOError:
        print >> sys.stderr, 'Error: No sites file ({}) to read'.format(
            RAW_SITES_FILE_PATH)
        
        sys.exit(2)

    try:
        change_hosts_file(sites)
    except ValueError as e:
        stop_getting_shit_done()
        start_getting_shit_done()
    except IOError:
        print >> sys.stderr, CANT_CHANGE_HOSTS_FILE_MESSAGE

        sys.exit(3)

def stop_getting_shit_done():
    try:
        restore_hosts_file()
    except ValueError:
        pass
    except IOError:
        print >> sys.stderr, CANT_CHANGE_HOSTS_FILE_MESSAGE 
        sys.exit(3)

if __name__ == '__main__':
    arguments = sys.argv[1:]

    try:
        if arguments[0] == u'start':
            start_getting_shit_done()
        elif arguments[0] == u'stop':
            stop_getting_shit_done()
    except IndexError:
        print >> sys.stderr, 'Usage: gsd.py <start|stop>'

        sys.exit(1)
