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
- SearchEngine

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
