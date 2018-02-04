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
        ip_check_result = ip_sanity_check(src_ip)

        if not ip_check_result['status']:
            sys.stderr.write(
                '[Warning] The src_ip "{}" is invalid; Skip line;'.format(src_ip)
            )
            continue

        if ip_check_result['ip'].ip in ip.network:
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
            print err


def ip_sanity_check(ip):
    """
    Checks that an ip or a network is valid.
    Returns a dict with fields:
        status - bool; True if valid, False if not;
        msg - str or None; message for print out;
        ip - ipaddress.IPv{4,6}Interface object or None
    """
    try:
        ip = ipaddress.ip_interface(u'{}'.format(ip))

    except ValueError:
        return {
            'status': False,
            'msg': '[Error 1] "{}" is invalid ip or network'.format(ip),
            'ip': None
        }

    return {'status': True, 'msg': None, 'ip': ip}


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

    ip_check_result = ip_sanity_check(args.ip)
    if not ip_check_result['status']:
        sys.exit(ip_check_result['msg'])

    process_log_files(ip_check_result['ip'], args.logfile)
