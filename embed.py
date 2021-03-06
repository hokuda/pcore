#!/usr/bin/python3
import sys
import re
import base64
import zlib
import subprocess


def get_version_info():
    try:
        git_log_command = "git log --date local"
        git_log_output = str(subprocess.check_output(git_log_command.split())).split('\\n')
        date_line = git_log_output[2].replace("Date:", "").strip()
        comment_line = git_log_output[4].strip()
        return date_line + " (" + comment_line + ")"
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            sys.stderr.write("This is not a valid git repository.\n")
            sys.stderr.write("Please git-clone at first:\n")
            sys.stderr.write("  $ git clone https:/github.com/hokuda/pcore.git\n")
            sys.stderr.write("then, build:\n")
            sys.stderr.write("  $ cd pcore\n")
            sys.stderr.write("  $ make # rhel7\n")
            sys.stderr.write("  or\n")
            sys.stderr.write("  $ make pcore.rhel8 # rhel8\n")
            sys.exit(1)
        raise(e)


def main():
    version_simple_pattern = "#VERSION#"
    version_info = get_version_info()
    getdebuginfo_regex_pattern = re.compile( r'^(.*)\'#EMBED (.*)#(.*)\'' )
    getdebuginfo_simple_pattern = "'#EMBED#'"
    getdebuginfo = sys.argv[1]
    with open(getdebuginfo, 'r') as fp:
        buf = fp.read()
        compressed = zlib.compress(buf.encode('utf-8'))
        b64enc = base64.standard_b64encode(compressed)
        chunks, chunk_size = len(b64enc), 64+9
        folded_b64enc = '\\\n    '.join(["'{}'".format(b64enc[i:i+chunk_size].decode(encoding='utf-8')) for i in range(0, chunks, chunk_size) ])
    for line in sys.stdin:
        line = line.replace(version_simple_pattern, version_info, 1)
        line = line.replace(getdebuginfo_simple_pattern, folded_b64enc, 1)
        print(line, end="")
    
if __name__ == '__main__':
    main()

