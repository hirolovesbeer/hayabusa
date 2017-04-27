import argparse
import subprocess

BASE_DIR = '/path/to/data'

def exec(time, match, count, verbose):
    if count:
        cmd = 'parallel sqlite3 ::: %s/%s ::: "select count(*) from syslog where logs match \'%s\';"' % (BASE_DIR, time, match)
        # debug code
        # cmd = 'parallel sqlite3 ::: /mnt/ssd1/benchmark-db/100k/100k-1.db ::: "select count(*) from syslog where logs match \'noc\';"'
    else:
        cmd = 'parallel sqlite3 ::: %s/%s ::: "select * from syslog where logs match \'%s\';"' % (BASE_DIR, time, match)
        # debug code
        # cmd = 'parallel sqlite3 ::: /mnt/ssd1/benchmark-db/100k/100k-1.db ::: "select * from syslog where logs match \'noc\';"'

    if verbose:
        print(cmd)

    subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--time",
                        help="time explain regexp(YYYY/MM/DD/HH/MIN). eg: 2017/04/27/10/*")
    parser.add_argument("--match",
                        help="matching keyword. eg: noc or 'noc Login'")
    parser.add_argument("-c",
                        help="count", action="store_true")
    parser.add_argument("-v",
                        help="verbose", action="store_true")
    parser.parse_args()

    args = parser.parse_args()

    exec(args.time, args.match, args.c, args.v)
