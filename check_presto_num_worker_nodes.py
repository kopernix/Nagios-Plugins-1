#!/usr/bin/env python
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2017-09-22 16:55:57 +0200 (Fri, 22 Sep 2017)
#
#  https://github.com/harisekhon/nagios-plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Nagios Plugin to check the number of Presto SQL worker nodes via the Coordinator API

Coordinator nodes do not show up in the worker node count

Thresholds apply to the minimum number of worker nodes to expect

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import traceback
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import UnknownError, support_msg_api, isList, plural
    from harisekhon import RestNagiosPlugin
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


class CheckPrestoWorkerNodeCount(RestNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckPrestoWorkerNodeCount, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = ['Presto Coordinator', 'Presto']
        self.default_port = 8080
        self.auth = False
        self.json = True
        self.path = '/v1/node'
        self.msg = 'Presto msg not defined'

    def add_options(self):
        super(CheckPrestoWorkerNodeCount, self).add_options()
        self.add_thresholds(default_critical=1)

    def process_options(self):
        super(CheckPrestoWorkerNodeCount, self).process_options()
        self.validate_thresholds(simple='lower')

    def parse_json(self, json_data):
        if not isList(json_data):
            raise UnknownError('non-list returned by Presto for nodes. {0}'.format(support_msg_api()))
        num_worker_nodes = len(json_data)
        self.msg = 'Presto SQL worker nodes = {0}'.format(num_worker_nodes)
        self.check_thresholds(num_worker_nodes)
        self.msg += ' | num_worker_nodes={0}{1}'.format(num_worker_nodes, self.get_perf_thresholds('lower'))


if __name__ == '__main__':
    CheckPrestoWorkerNodeCount().main()