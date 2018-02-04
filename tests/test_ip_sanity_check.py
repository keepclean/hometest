#!/usr/bin/env python

import os
import pytest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from weblog_helper import ip_sanity_check


class TestIpSanityCheck:

    def test_invalid_ipv4_address(self):
        with pytest.raises(ValueError):
            ip_sanity_check(u'192.168.1.1000')

    def test_invalid_ipv6_address(self):
        with pytest.raises(ValueError):
            ip_sanity_check(u'::g')

    def test_invalid_ipv4_network(self):
        with pytest.raises(ValueError):
            ip_sanity_check(u'192.168.1.0/33')

    def test_invalid_ipv6_network(self):
        with pytest.raises(ValueError):
            ip_sanity_check(u'::1/129')
