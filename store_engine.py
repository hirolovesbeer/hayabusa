import configparser
import os.path
import sqlite3

import datetime
from distutils.dir_util import mkpath

LOG_FILE = '/var/log/messages.1'
BASE_DIR = '/var/tmp/data'
CONFIG   = '/path/to/config.ini'

def main():
    now = datetime.datetime.now()
    dir_path = '%d/%02d/%02d/%02d' % (now.year, now.month, now.day, now.hour)
    db_file = '%d.db' % (now.minute)
    db_path = '%s/%s/%s' % (BASE_DIR, dir_path, db_file)

    dir_path = '%s/%s' %(BASE_DIR, dir_path)
    mkpath(dir_path)

    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE VIRTUAL TABLE SYSLOG USING FTS3(LOGS)");
        conn.close()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA SYNCHRONOUS = OFF");
    conn.execute("PRAGMA JOURNAL_MODE = MEMORY");

    with open(LOG_FILE, "r", encoding="utf-8", errors='ignore') as fh:
        lines = [[line] for line in fh]

        try:
            conn.executemany('INSERT INTO SYSLOG VALUES( ? )', lines)
        except sqlite3.Error as e:
            print(e)
        else:
            conn.commit()

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG)

    LOG_FILE = config['path']['log-file']
    BASE_DIR = config['path']['base-dir']

    main()
