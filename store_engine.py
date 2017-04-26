import os.path
import sqlite3

log_file = '/var/log/message.1'
db_file = 'test.db'

if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute("CREATE VIRTUAL TABLE SYSLOG USING FTS3(LOGS)");
    conn.close()

conn = sqlite3.connect(db_file)
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
