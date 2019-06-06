import requests
import sys
import time


from pxrest import *


session = Session('orca-connect.lab.plexxi.com')  # address or hostname of CFM
session.authenticate()

switches_response = session.send_request('GET', 'switches')

# No sorting of switches by name yet - order undefined
for switch in switches_response['result']:
    # Should build and send a "GET /ports?switches=<switch_uuid>&type=access"
    ports = session.send_request('GET', 'ports', params = {'switches': switch['uuid'], 'type': 'access'})
    print '=========== {} ============'.format(switch['name'])

    # No sorting of ports by label - order undefined
    for i, port in enumerate(ports['result']):
        # Pull out and display selected fields for the port
        print '{:>10} {:>6} {:>8} {:>8}'.format(port['port_label'],
                                                port['speed']['current'],
                                                port['admin_state'],
                                                port['link_state'])
    print '=========================='
