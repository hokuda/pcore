#!/usr/bin/python
import sys
import re
import base64
import zlib
import subprocess


def get_version_info():
    git_log_command = "git log --date local"
    git_log_output = str(subprocess.check_output(git_log_command.split())).split('\n')
    date_line = git_log_output[2].replace("Date:", "").strip()
    comment_line = git_log_output[4].strip()
    return date_line + " (" + comment_line + ")"


def main():
    version_simple_pattern = "#VERSION#"
    version_info = get_version_info()
    getdebuginfo_regex_pattern = re.compile( r'^(.*)\'#EMBED (.*)#(.*)\'' )
    for line in sys.stdin:
        m = getdebuginfo_regex_pattern.match(line)
        if m:
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
            line = line.replace(version_simple_pattern, version_info, 1)
            print line,
    
if __name__ == '__main__':
    main()

