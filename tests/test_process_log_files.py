#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from weblog_helper import process_log_files


class TestProcessLogFiles:

    def test_nonexistent_logfile(self, capfd):
        logfile = 'non_existent_logfile.txt'
        process_log_files('10.0.0.1', [logfile])

        out, err = capfd.readouterr()
        assert(
            out == "[Errno 2] No such file or directory: '{}'\n".format(
                logfile
            )
        )
