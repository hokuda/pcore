#!/usr/bin/python
import sys
import re

if __name__ == '__main__':
    pattern = re.compile( r'^(.*)#EMBED (.*)#(.*)' )
    match = False
    for line in sys.stdin:
        m = pattern.match(line)
        if m:
            match = True
            prefix = m.group( 1 )
            fp = open(m.group( 2 ), 'r')
            buffer = fp.read()
            fp.close()
            suffix = m.group( 3 )
            print '{0}{1}{2}'.format(prefix, buffer, suffix)
        else:
            print line,
