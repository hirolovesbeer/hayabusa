# Hayabusa
Hayabusa: A Simple and Fast Full-Text Search Engine for Massive System Log Data
[
# Concept
- Pure python implement
- Parallel SQLite processing engine
- SQLite3 FTS(Full Text Search) funstionaaa
- Core-scale architecture

# Architecture
- Design of the directory structure
  - By specifying a search range of time in ”the directory path + yyyy + mm + dd + hh + min.db”, the search program can select the search time systematically.
  ```
  /targetdir/yyyy/mm/dd/hh/min.db
  ```

- StoreEngine
  - sample code
  ```
  import os.path import sqlite3
  db_file = ’test.db’ log_file = ’1m.log’
  
  if not os.path.exists(db_file):
      conn = sqlite3.connect(db_file) conn.execute("CREATE VIRTUAL TABLE SYSLOG USING FTS3(LOGS)");
      conn.close()
  conn = sqlite3.connect(db_file)
  
  with open(log_file) as fh:
      lines = [[line] for line in fh] 
      conn.executemany(’INSERT INTO SYSLOG VALUES ( ? )’, lines) 
      conn.commit()
  ```

- SearchEngine
  - sample command
  ```
  $ parallel sqlite3 ::: target files ::: "select count(*) from xxx where logs match ’ keyword ’;" | awk ’{m+=$1} END{print m;}’

  Parallel Processing : parallel + sqlite command Aggregator : pipe(|) + shell script(awk)
  ```

- Architecture Image
![Hayabusa Architecture](./image/hayabusa-arch.png "hayabusa architecture image")

# Development Environment
- CentOS 7.3
- Python 3.5.1(use anaconda packages)
- SQLite3(version 3.9.2)

# Dependency Softwares
- Python 3
- SQLite3
- GNU Parallel

# Benchmark
- TBD
