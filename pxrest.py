import requests
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def timestamp_start():
    return time.time()

def timestamp_end(start_timestamp, name):
    pass
    # print '{}: {:.2f}'.format(name, time.time() - start_timestamp)

class Session:
    def __init__(self, host):
        self.host = host
        self.token = None

    def authenticate(self):
        headers = {
            'X-Auth-Username': 'admin',
            'X-Auth-Password': 'plexxi',
            'Content-Type': 'application/json'
        }
        r = requests.post('https://{}/api/v1/auth/token'.format(self.host), headers=headers, verify=False)

        r.raise_for_status()
        res = r.json()
        self.token = res.get('result')

    def send_request(self, method, path, json=None, params=None):
        headers = {
            'Authorization': self.token,
            'accept': 'application/json; version=1.0'
        }
        timestamp = time.time()
        url = 'https://{}/api/v1/{}'.format(self.host, path)
        if not params:
            params = dict()
        params.update(request_id=1)
        r = requests.request(method, url, json=json, headers=headers, verify=False, params=params, timeout=180.0)
        timestamp = time.time() - timestamp
        url_pretty = url
        param_count = 0
        for k, v in params.items():
            if k == 'request_id':
                continue
            elif param_count == 0:
                url_pretty += '?{}={}'.format(k, v)
            else:
                url_pretty += '&{}={}'.format(k, v)
            param_count += 1
        print '{}: {:.3f}s'.format(url_pretty, timestamp)
        if not r.ok:
            print str(r.json())
        r.raise_for_status()
        return r.json()


def get_ip_svi(vlan, primary, secondaries):
    ipv4_secondaries = [dict(address=elem[0], prefix_length=elem[1])
                        for elem in secondaries]
    return {
            "enable": True,
            "description": "Description of my IP Interface",
            "ipv4_secondary_addresses": ipv4_secondaries,
            "vlan": vlan,
            "ipv6_addresses": [],
            "ipv4_primary_address": {
                "prefix_length": primary[1],
                "address": primary[0]
            },
            "if_type": "vlan",
            "name": "My IP Interface"
    }

def make_bgp_global_put(as_number):
    return {
            'as_number': as_number,
            "holddown_timer": 90,
            "redistribute_static": True,
            "description": "Description of BGP global config",
            "redistribute_connected": True,
            "enable": True,
            "intra_fabric": {
                "holddown_timer": 90,
                "name": "My BGP switch",
                "authentication_password": "",
                "mode": "disabled",
                "keepalive_timer": 30,
                "switches": [],
                "description": "Description of BGP switch"
            },
            "keepalive_timer": 30,
            "redistribute_ospf": True,
            "switches": [
            ],
            "name": "My BGP global config"
        }

def make_bgp_neighbor_put(neighbor_as_number, neighbor_ip, filter_list_in=None, filter_list_out=None):
    return {
        'holddown_timer': 90,
        'description': 'Description of BGP neighbor',
        'weight': 1,
        'neighbor_as_number': neighbor_as_number,
        'neighbor_ip_address': '192.168.1.1',
        'authentication_password': '',
        'route_reflector_client': False,
        'route_filter_list_out': filter_list_out,
        'keepalive_timer': 30,
        'address_families': [
          'ipv4'
        ],
        'route_filter_list_in': filter_list_in,
        'name': 'My BGP neighbor',
        'soft_reconfiguration_inbound': False
    }

def make_bgp_switch_put(router_id, neighbours, networks):
    return {
            "router_id": router_id,
            "neighbors": neighbours,
            "holddown_timer": 90,
            "redistribute_static": True,
            "description": "Description of BGP switch",
            "redistribute_connected": True,
            "keepalive_timer": 30,
            "redistribute_ospf": False,
            "networks": networks,
            "name": "My BGP switch"
    }



def patch_ports(session, port_uuids, params):
    patch_body = {
        'uuids': list(port_uuids),
        'patch': [dict(path=k, value=v, op='replace') for k, v in params.items()]
    }
    response = session.send_request('PATCH', 'ports', json=[patch_body])

def create_ip_svis(session, vpc_uuid, ip_svis):
    post_body = ip_svis
    response = session.send_request('POST', 'vpcs/{}/ip_interfaces'.format(vpc_uuid), json=post_body)

def create_lag(session, lag_port_uuids, name, vlan_group_uuids=None, native_vlan=1, port_speed=1000):
    lag_post_body = {
    "native_vlan": native_vlan,
    "description": "",
    "vlan_group_uuids": vlan_group_uuids or [],
    "port_properties": [
    {
        "lacp": {
            "priority": 100,
            "intervals": {
                "slow": 30,
                "fast": 1
            },
            "aggregate_port_limits": {
                "minimum": 2,
                "maximum": 8
            },
            "mode": "active"
        },
        "speed": {
            "current": port_speed
        },
        "port_uuids": lag_port_uuids
    }
    ],
    "lacp_fallback": {
        "port_uuid": lag_port_uuids[0],
        "timeout": 30
    },
    "ungrouped_vlans": "",
    "name": name
    }
    response = session.send_request('POST', 'lags', json=lag_post_body)
    return response['result']


def create_vlan_group(session, vlans, vlan_group_name):
    post_body = {
      "description": "",
      "name": vlan_group_name,
      "vlans": vlans
    }
    response = session.send_request('POST', 'vlan_groups', json=post_body)
    return response['result']

def get_access_ports_for_switch(session, switch_uuid):
    switch_param = '{}'.format(switch_uuid)
    response = session.send_request('GET', 'ports', params = {'switches': switch_param, 'type': 'access'})
    ports = [port['uuid'] for port in response['result']]
    return ports

def get_lag_uuids(session):
    response = session.send_request('GET', 'lags', params = {'type': 'provisioned'})
    return [lag['uuid'] for lag in response['result']]

def get_vlan_group_uuids(session):
    response = session.send_request('GET', 'vlan_groups')
    return [vg['uuid'] for vg in response['result']]

def delete_lag(session, lag_uuid):
    session.send_request('DELETE', 'lags/{}'.format(lag_uuid))

def delete_vlan_group(session, vg_uuid):
    session.send_request('DELETE', 'vlan_groups/{}'.format(vg_uuid))

