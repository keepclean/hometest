#!/usr/bin/env python

import argparse
import ipaddress
import sys


class InvalidIpError(Exception):
    """ Custom exception """
    pass


def find_lines(ip, logfile):
    """
    Searches and prints lines that match for ip or network
    """
    for lineno, line in enumerate(logfile, start=1):
        src_ip, _ = line.split(None, 1)

        try:
            parsed_src_ip = ip_sanity_check(src_ip)
        except InvalidIpError as err:
            sys.stderr.write(
                '[{}] Skipped the line number {}: {}'.format(
                    logfile.name,
                    lineno,
                    err
                )
            )
            continue

        if parsed_src_ip.ip in ip.network:
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
        parsed_ip = ipaddress.ip_interface(unicode(ip))
    except ValueError:
        raise InvalidIpError(
            '{} is not a valid ip address or network'.format(ip)
        )

    return parsed_ip


def main():
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
    except InvalidIpError as err:
        sys.exit(err)

    process_log_files(ip, args.logfile)


if __name__ == '__main__':
    main()
