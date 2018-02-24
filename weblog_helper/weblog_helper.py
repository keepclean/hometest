#!/usr/bin/env python

import argparse
import ipaddress
import heapq
import operator
import sys


class InvalidIpError(Exception):
    """ Custom exception """
    pass


def find_top_ips(logfile, **args):
    top_n = args['top']
    ip_entries = dict()

    for line in logfile:
        src_ip, _ = line.split(None, 1)

        try:
            parsed_src_ip = str(parse_ip(src_ip).ip)
        except InvalidIpError as err:
            sys.stderr.write(
                '[{}] Skipped invalid ip: {}'.format(
                    logfile.name, err
                )
            )
            continue

        ip_entries.setdefault(parsed_src_ip, 0)
        ip_entries[parsed_src_ip] += 1

    top_n_entries = heapq.nlargest(top_n, ip_entries.iteritems(), operator.itemgetter(1))
    sys.stdout.write('Log: {}\nSource ip\t\tHits\n'.format(logfile.name))
    for ip, hits in top_n_entries:
        sys.stdout.write('{}\t\t{}\n'.format(ip, hits))


def find_lines(logfile, **args):
    """
    Searches and prints lines that match for ip or network
    """
    ip_to_find = args['ip']
    for lineno, line in enumerate(logfile, start=1):
        src_ip, _ = line.split(None, 1)

        try:
            parsed_src_ip = parse_ip(src_ip)
        except InvalidIpError as err:
            sys.stderr.write(
                '[{}] Skipped the line number {}: {}'.format(
                    logfile.name,
                    lineno,
                    err
                )
            )
            continue

        if parsed_src_ip.ip in ip_to_find.network:
            sys.stdout.write(line)


def process_log_files(func, logfiles, **args):
    """
    Iterates through a log files list and calls find_lines function for search proper lines
    """
    for logfile in logfiles:
        try:
            with open(logfile) as lf:
                # call function which specified in func variable
                func(lf, **args)
        except Exception as err:
            sys.stderr.write('{}: {}\n'.format(
                err.strerror,
                err.filename
            ))


def parse_ip(ip):
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
        type=str,
        help='''ip address or network for search in log file;
        e.g. --ip 10.0.0.1 or --ip 10.0.0.1/24'''
    )
    parser.add_argument(
        '--top-ips',
        type=int,
        help='''print N top ip address from each log file'''
    )
    parser.add_argument(
        'logfile',
        type=str,
        nargs='+',
        help='log files for searching'
    )
    args = parser.parse_args()

    if args.ip:
        try:
            ip = parse_ip(args.ip)
        except InvalidIpError as err:
            sys.exit(err)

        process_log_files(find_lines, args.logfile, ip=ip)

    elif args.top_ips:
        process_log_files(find_top_ips, args.logfile, top=args.top_ips)


if __name__ == '__main__':
    main()
