#!/usr/bin/env python

import ipaddress
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../weblog_helper"))
from weblog_helper import find_lines


class TestFindLines:
    def test_correct_line(self, capfd):
        ip = ipaddress.ip_interface(u"31.184.238.128")
        with open("tests/logfile.txt") as lf:
            find_lines(ip, lf)

        out, err = capfd.readouterr()
        assert out == "31.184.238.128 - -\n"

    def test_uncorrect_line(self, capfd):
        ip = ipaddress.ip_interface(u"31.184.238.128")
        with open("tests/logfile.txt") as lf:
            find_lines(ip, lf)

        out, err = capfd.readouterr()
        assert (
            err
            == "[tests/logfile.txt] Skipped the line number 2: 31.184.238.128/33 is not a valid ip address or network"
        )
