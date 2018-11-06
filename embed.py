#!/usr/bin/python
import sys
import re
import base64
import zlib

def main():
    pattern = re.compile( r'^(.*)#EMBED (.*)#(.*)' )
    match = False
    for line in sys.stdin:
        m = pattern.match(line)
        if m:
            match = True
            prefix = m.group( 1 )
            fp = open(m.group( 2 ), 'r')
            buf = fp.read()
            fp.close()
            compressed = zlib.compress(buf.encode('utf-8'))
            b64enc = base64.standard_b64encode(compressed)
            chunks, chunk_size = len(b64enc), 64+9
            s = '\\\n    '.join(["'{}'".format(b64enc[i:i+chunk_size]) for i in range(0, chunks, chunk_size) ])
            suffix = m.group( 3 )
            print '{0}{1}{2}'.format(prefix, s, suffix)
        else:
            print line,
    
if __name__ == '__main__':
    main()

