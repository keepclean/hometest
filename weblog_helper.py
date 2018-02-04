#!/usr/bin/env python

import argparse
import ipaddress
import sys


def find_lines(ip, logfile):
    """
    Searches and prints lines that match for ip or network
    """
    for line in logfile:
        src_ip, _ = line.split(None, 1)

        try:
            src_ip = ip_sanity_check(src_ip)
        except ValueError:
            sys.stderr.write(
                '[Warning] The src_ip "{}" is invalid; Skip line;\n'.format(src_ip)
            )
            continue

        if src_ip.ip in ip.network:
            sys.stdout.write(line)


def process_log_files(ip, logfiles):
    """
    Iterates through a log files list and calls find_lines function for search proper lines
    """
    for logfile in logfiles:
        try:
            with open(logfile) as lf:
                find_lines(ip, lf)
        except Exception as err:
            sys.stderr.write('{}: {}\n'.format(
                err.strerror,
                err.filename
            ))


def ip_sanity_check(ip):
    """
    Checks that an ip or a network is valid.
    Returns ipaddress.IPv{4,6}Interface object
    """
    try:
        ip = ipaddress.ip_interface(unicode(ip))
    except ValueError:
        raise

    return ip


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True,
        description='Returns all log lines that correspond to a given source IP address or CIDR network'
    )
    parser.add_argument(
        '--ip',
        required=True,
        type=str,
        help='ip address or network for search in log file'
    )
    parser.add_argument(
        'logfile',
        type=str,
        nargs='+',
        help='log files for searching'
    )
    args = parser.parse_args()

    try:
        ip = ip_sanity_check(args.ip)
    except ValueError:
        sys.exit('[Error] "{}" is invalid ip or network'.format(args.ip))

    process_log_files(ip, args.logfile)
