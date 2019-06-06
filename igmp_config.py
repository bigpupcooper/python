# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2017, Plexxi Inc. and its licensors.
#
# All rights reserved.
#
# Use and duplication of this software is subject to a separate license
# agreement between the user and Plexxi or its licensor.
#
##########################################################################

"""
This script can be used to configure the IGMP snooping settings for a given vlan

Usage:
  igmp_config [options] -n name
  igmp_config --help

Options:
  -h --help                  Show this screen
  -u --user <username>       Set the username [default: admin]
  -p --password <password>   Set the password [default: plexxi]
  -n --name <dns>            The DNS name or IP to connect to
  --igmp <igmp>              IGMP snooping value
  --vlan <vlan>              The VLAN to use.
  --preview                  Print current configuration
"""

import requests
import sys
import traceback
import re

from docopt import docopt
from plexxi.core.api import binding, session, util
from plexxi.control.api.binding import Vlan as PybVlan

requests.packages.urllib3.disable_warnings()


def convert_string_range_to_int(str_range):
    """
    Returns a list of integers from a string range.
    '1,2-5' returns [1,2,3,4,5]

    :param str str_range:    String of ranges
    :return:                 A list of ints
    """
    range_list = str_range_to_list(str_range)
    return map(int, range_list)

def str_range_to_list(str_range):
    """
    Convert a string ranges to list. Supports prefixes.
    '1,2-5' returns ['1','2','3','4','5']
    '1,xe1-xe5' returns ['1','xe1','xe2','xe3','xe4','xe5']
    """
    range_list = []
    for i in str_range.split(','):
        l, r = i.split('-')[0], i.split('-')[-1]
        p = re.search('\d', l).start()
        for x in range(int(l[p:]), int(r[p:]) + 1):
            range_list.extend(['%s%s' % (l[0:p], x)])

    return range_list


if __name__ == '__main__':
    arguments = docopt(__doc__, help=True)

    plexxi_session = None

    try:
        # connect to Plexxi Control
        plexxi_session = session.CoreSession.connect('http://{}:8080/PlexxiCore/api'.format(arguments['--name']), True,
                                                     arguments['--user'],
                                                     arguments['--password'])
    except requests.exceptions.HTTPError as http_error:
        error_code = int(http_error.response.status_code)
        if error_code == 401:
            print 'Connection failed due to authentication failure.'
        else:
            print 'Connection failed (ErrorCode={}).'.format(error_code)
        sys.exit(1)
    except requests.exceptions.ConnectionError as connect_error:
        print 'Connection failed (ErrorMessage={}).'.format(connect_error.message)
        sys.exit(1)
    except Exception as e:
        print 'Connection unexpectedly failed ({}).'.format(e.message)
        traceback.format_exc()
        sys.exit(1)
    
    vlan = convert_string_range_to_int(arguments['--vlan'])

    igmp_snooping = arguments['--igmp']

    default_multicast_settings = {'igmp_snooping_enabled': igmp_snooping,
                                      'igmp_snooping_querier_timeout': 126,
                                      'igmp_snooping_reporter_timeout': 261,
                                      'ingress_multicast_squelch': 'none',
                                      'egress_multicast_squelch': 'none'}
    squelch_map = {'none': 'NONE', 'all': 'ALL', 'most': 'MOST'}
    job = binding.Job.create(name='Configuring IGMP Snooping',
                                     description='Configuring IGMP Snooping')
    job.begin()
    for v in vlan:
        pyb_vlan_props = PybVlan.getPropertiesByVlanId(int(v))
        pyb_vlan_props.setIgmpSnoopingEnabled(igmp_snooping)
        
        pyb_vlan_props.addVlanId(int(v))
        PybVlan.setProperties(pyb_vlan_props)

    job.commit()