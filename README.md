# hometest
Returns all log lines that correspond to a given source IP address or CIDR
network

**Usage**:
```sh
weblog_helper.py [-h] --ip IP logfile [logfile ...]
```

```
Positional arguments:
    logfile     log files for searching

Optional arguments:
    -h, --help  show this help message and exit
    --ip IP     ip address or network for search in log file; e.g. --ip 10.0.0.1 or --ip 10.0.0.1/24
```
