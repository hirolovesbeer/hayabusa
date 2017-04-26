import os.path
import sqlite3

import datetime
from distutils.dir_util import mkpath

log_file = '/var/log/message.1'

now = datetime.datetime.now()
dir_path = '%d/%02d/%02d/%02d ' % (now.year, now.month, now.day, now.hour)
db_file = '%.db' % now.minute
db_path = dirpath + '/' + db_file

mpkath(dir_path)

if not os.path.exists(db_path):
    conn = sqlite3.connect(db_file)
    conn.execute("CREATE VIRTUAL TABLE SYSLOG USING FTS3(LOGS)");
    conn.close()

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA SYNCHRONOUS = OFF");
conn.execute("PRAGMA JOURNAL_MODE = MEMORY");

with open(log_file) as fh:
    lines = [[line] for line in fh]

    try:
        conn.executemany('INSERT INTO SYSLOG VALUES( ? )', lines)
    except sqlite3.Error, e:
        print(e)
    else:
        conn.commit()
