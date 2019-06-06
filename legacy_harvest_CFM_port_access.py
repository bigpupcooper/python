import requests
import sys
import time
import pickle
from pprint import pprint as pp
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Set the Connect IP address
nonCFM_HOST_IP = '172.18.24.172' # 3.1 Connect - NOT Control
CFM_HOST_IP = '172.18.24.160' #CFM Connect


#Create a class and the only variable we pass in is the host address

class Session:
    def __init__(self, host):
        self.host = host
        #self.token = None

# In this function call we get the token for the Connect server, nothing is passed in.
    def authenticate(self):
        headers = {
            'X-Auth-Username': 'admin',
            'X-Auth-Password': 'plexxi',
            'Content-Type': 'application/json'
        }
        r = requests.post('https://{}/api/v1/auth/token'.format(self.host), headers=headers, verify=False, timeout = 5.0)
        r.raise_for_status()
        res = r.json()
        #Not sure as to why we don't have "return here"
        self.token = res.get('result')

# This is the request to send using a method (GET, PUT etc) and a path eg. "nonCFM_session.send_request('GET', 'switches')"

    def send_request(self, method, path, json=None, params=None):
        headers = {
            'Authorization': self.token,
            'accept': 'application/json; version=1.0'
        }

        #Path to the end point
        url = 'https://{}/api/v1/{}'.format(self.host, path)        

        r = requests.request(method, url, json=json, headers=headers, verify=False)
        return r.json()
        
#pass in the json to this function
def get_switch_macs(response):
    """ Get the switch MACs, and return a list of MACs"""
    switch_macs = []
    for switch in response['result']:
        mac = switch.get('mac_address')
        switch_macs.append(mac)
    #return the variable switch_macs out from the function
    return switch_macs

# 

def get_fabric(response):
    """Get the fabric information- is whole, description, name, uuid, count
       return a string of fabric name and fabric description"""

    fab_info = []
    for fabric in response['result']:
        fab_desc = fabric.get('description')
        fab_uuid = fabric.get('uuid')
        fab_name = fabric.get('name')
        

    return fab_name, fab_desc

def get_switch_name(response):
    """Get the switch name, and return a list of switch names"""

    switch_name = []
    for switch in response['result']:
        name = switch.get('name')
        switch_name.append(name)
    return switch_name

def get_switch_model(response):
    """Get the switch model, and return a list of switch models"""

    switch_model = []
    for switch in response['result']:
        model = switch.get('model')
        switch_model.append(model)
    return switch_model

def get_lag_loop(response):
    """Get the lag information, return the lag description, name and speed"""

    lag_info = []
    for lag in response['result']:
        lag_port_desc = lag.get('description')
        lag_port_name = lag.get('name')
        lag_speed = lag.get('speed')
        #print '{:>5} {:5<}'.format(lag_port_name, lag_port_desc)
    return lag_port_desc, lag_port_name, lag_speed

def get_switch_uuid(response):
    """Get the switch UUID, and return a list of them"""

    switch_uuid = []
    for switch in response['result']:
        sw_uuid = switch.get('uuid')
        switch_uuid.append(sw_uuid)
    return switch_uuid

def get_switch_ip(response):
    """Get the switch IPs and return a list of them"""

    switch_ip = []
    for switch in response['result']:
        sw_ip = switch.get('ip_address')
        switch_ip.append(sw_ip)
    return switch_ip




def get_ports_for_switch(sw_uuid):  
    """For each of the switch UUIDs, this function is being used to extract the port information and print it
        nicely to screen, it returns a list of port information for each switch"""

    nonCFM_session = Session(nonCFM_HOST_IP)  # address or hostname of CFM
    nonCFM_session.authenticate()

    switch_list = []
    for uuid in sw_uuid:
        port_response = nonCFM_session.send_request('GET', 'ports?switches=' + uuid)
        switch_list.append(port_response)
    # the list now has dicts inside it

    #now iterate through each one of the dicts and pull back a list of values from result, this should be one list (sw_info) per switch length of ports(72)
        for sw_dict in switch_list:
            sw_info= sw_dict.get('result')
          
            print '\n'
            print '{:^18} {:^5} {:^10} {:^15} {:^15} {:^8} {:^6} {:^5} {:^15} {:^15}'.format('SW Name', 'Label', 'Admin', 'Desc', 
                                                                                            'Name', 'Access', 'Native', 'Link',
                                                                                            'Current Speed', 'Vlan')
            print '\n'

            #iterate thru each element of the list (will get you data for each of the ports)
            for port in sw_info:
                port_label = port.get('port_label')
                port_admin = port.get('admin_state')
                switch_name = port.get('switch_name')
                port_name = port.get('name')
                port_desc = port.get('description') 
                port_type = port.get('access_port')
                port_native_vlan = port.get('native_vlan')
                port_link_state = port.get('link_state')
                port_speed = port.get('speed')
                port_current_speed = port_speed.get('current')
                port_vlan = port.get('vlans')
                print '{:^18} {:^5} {:^10} {:^15} {:^15} {:^8} {:^6} {:^5} {:^15} {:^15}'.format(switch_name, port_label, port_admin, 
                                                                            port_desc, port_name, port_type, port_native_vlan, 
                                                                            port_link_state, port_current_speed, port_vlan)
                  

    return switch_list 
  

def get_connect_switch(sw_uuid):
    """For Connect: get a list of all the switches and data from call for access ports and return as a list 
    containing a dict per switch, and also a list of port count per switch"""

    nonCFM_session = Session(nonCFM_HOST_IP)  # address or hostname of CFM
    nonCFM_session.authenticate()
    
    nonCFM_switch_list_access = []
    nonCFM_port_count_list = []

    for switch in sw_uuid:
        port_response = nonCFM_session.send_request('GET', 'ports?switches=' + switch +'&type=access') #For ACCESS PORTS only
        nonCFM_switch_list_access.append(port_response)
        con_port_count = len(port_response.get('result'))
        nonCFM_port_count_list.append(con_port_count)
    print "This is the port count list for Connect\n"
   
    return nonCFM_switch_list_access, nonCFM_port_count_list

def get_CFM_switch(sw_uuid):
    """ For CFM: get a list of all the switches and data from call for access ports and return as a 
    list containing a dict per switch, and also a list of port count per switch"""

    CFM_session = Session(CFM_HOST_IP)  # address or hostname of CFM
    CFM_session.authenticate()
    
    CFM_switch_list_access = []
    cfm_port_count_list = []
    for switch in sw_uuid:
        port_response = CFM_session.send_request('GET', 'ports?switches=' + switch +'&type=access') #For ACCESS PORTS only
        port_count = len(port_response.get('result'))
        cfm_port_count_list.append(port_count)
        CFM_switch_list_access.append(port_response)

    print "This is the port count from CFM per switch: \n"
   
    return CFM_switch_list_access, cfm_port_count_list
        
def strip_switch_data(switch_list): # paul k wrote this
    """ Takes the list of all switches from get_connect switch, creates a reduced list of name, uuid, and label """
    switch_count = len(switch_list) 
    # "sw" is a dictionary of length 3 ie - count, result, time
    
    new_dict = {} # create a new dictionary 
    
    for sw in switch_list:
        sw_info= sw.get('result') # creates a list of items from a dict. Is a list of length 48 (number of access ports per switch)
        switch_name = sw_info[0].get('switch_name') # take the first element of the list of 48 and get the switch name from it
        new_dict[switch_name] = [] # Assign switchname  eg. mydict[key] = "value" . This creates a placeholder list, so rupert [], and then drop into the port loop to populate, then bob[] etc
        # the Key is the switchname, and the value is a list of dictionaries for each port and contains port label and uuid

       

        for port in sw_info: # 0-47 for each switch
            port_info = {
                'label': int(port.get('port_label')), #need to int, as CFM portlabel is unicode, and sort fails
                'uuid': port.get('uuid'),
                'name': port.get('name'),
                'description': port.get('description')
                }
            new_dict[switch_name].append(port_info)
            
        
    return new_dict 

def order_dict_on_label(new_dict):
    """"This function takes the dictionary of switches and then sorts each by their port label and rolls back up into a dict"""
    
    ordered_port_dict = {}

    for name in new_dict:
        ordered_port_dict[name] = sorted(new_dict[name], key=lambda k: k['label'])
    return ordered_port_dict



def get_fab_resp(): #TODO Tidy this up, there is no need for sw_response, lag_repsonse
    
    nonCFM_session = Session(nonCFM_HOST_IP) 
    nonCFM_session.authenticate()
    
    sw_response = nonCFM_session.send_request('GET', 'switches') 
    lag_response = nonCFM_session.send_request('GET', 'lags?port_type=access&type=provisioned' )
    fab_response = nonCFM_session.send_request('GET', 'fabrics')
    fab_count = fab_response['count']
    return fab_count

def check_both_servers(session):
    """code up a check to make sure that both Connect and CFM is online and CFM has no fabric configured (clean)
       and that Connect has only one fabric"""
    
    nonCFM_fab = get_fab_resp() # Get the count of fabrics in Connect
    
    check_CFM_fab_resp = session.send_request('GET','fabrics')
    CFM_fab = check_CFM_fab_resp.get('count')
    
    
    if nonCFM_fab > 2: # Change this back to 1
        print ' ********** Error: Detected more than one fabric for Connect ' + str(nonCFM_HOST_IP) + ' *************'
        return False
    elif CFM_fab != 0: # Change back to 0 
        print ' ********* Error: Detected a fabric is already configured for CFM ' +str(CFM_HOST_IP) + ' ************'
        return False
    else: 
        print 'Good to start as you have one fabric in Connect and zero configured in CFM'
        return True

    


def add_fabric(session, switch, fabric_name, fabric_desc):
    """Function to create a new fabric and return the response from CFM."""

    provision_fabric = raw_input('Do you wish to create a fabric on CFM? : yes / no ')

    if provision_fabric == 'yes':
        
        post_body = {
        "host": switch,
        "name": fabric_name,
        "description": fabric_desc
        }
        response = session.send_request('POST', 'fabrics', json=post_body)
        print response.items()
        return response['result']
    
    elif provision_fabric == 'no' :      
        return 'Come back later'

def set_cfm_port_info(session,cfm_ports,connect_ports,switch_name,number_of_ports_list):
    """ Pass in CFM session, ordered port list from CFM to get port UUID"""
    
    # Need to match the port label from connect and cfm <- Use index of switchlist 0 = port 1, 47 = port 48
 #   print cfm_ports
    print switch_name
    port_int =  number_of_ports_list[0]
    print port_int
    
    for switch in switch_name:
        print switch
        for port in range(port_int):
            #print port
            puuid = [cfm_ports[switch][port]['uuid']]
            pname = [connect_ports[switch][port]['name']]
            pdesc = [connect_ports[switch][port]['description']]
            sample_output = {"uuids":str(puuid[0]),
                "patch":[{"op":"replace","path":"/name","value":str(pname[0])},
                {"op":"replace","path":"/description","value":str(pdesc[0])}]}
            print sample_output


    post_body = [{"uuids":[cfm_ports['admin-vs1'][0]['uuid']],
                "patch":[{"op":"replace","path":"/name","value":"rrrrtttttrle"},
                {"op":"replace","path":"/description","value":"rrrttttrrle"}]}]

      
    response = session.send_request('PATCH', 'ports', json=post_body)

    return response['result']

def compare_port_counts (connect_port_list, cfm_port_list):
    """ This function checks to make sure the access port counts for all cfm created switches match connect"""

    if connect_port_list != cfm_port_list:
        sys.exit("Port counts don't match")
    
    else:
        print "Port counts match"
        return True


# TODO function to read back the UUIDs for CFM switches

def main():
    #Put the session for host and authenticate here so you dont need to repeat for every function call
    nonCFM_session = Session(nonCFM_HOST_IP) 
    nonCFM_session.authenticate()
    CFM_session = Session(CFM_HOST_IP)
    cfm_auth = CFM_session.authenticate()
    #TODO uncomment the below two lines if you already have a fabric
    #if check_both_servers(CFM_session) == False: # Check that there is only one fabric on Connect and zero on CFM.
     #   exit()

    sw_response = nonCFM_session.send_request('GET', 'switches') 
    lag_response = nonCFM_session.send_request('GET', 'lags?port_type=access&type=provisioned' )
    fab_response = nonCFM_session.send_request('GET', 'fabrics')
    fab_count = fab_response['count']

    #Do some serialization using pickle module with sw_response on nonCFM
    pickle_out = open("noncfm_switches.tmp", "wb")
    pickle.dump(sw_response, pickle_out)
    pickle_out.close()

    cfm_switch_response = CFM_session.send_request('GET', 'switches')
     
    switch_count = sw_response['count']
    print switch_count
    print get_switch_macs(sw_response)
    print get_switch_name(sw_response)
    print get_switch_model(sw_response)
    #print get_lag_loop(lag_response) #TODO There is an error here when - local variable assigned logic
    print get_switch_uuid(sw_response)
    print get_switch_ip(sw_response)
    #Pull back the switch uuid than can be used an passed to GET for Port UUID information
    switch_uuid = get_switch_uuid(sw_response)
    get_ports_for_switch(switch_uuid)

  #TODO- Someting to look at below with two switch_list assignments###############
    switch_list = get_ports_for_switch(switch_uuid)
    switch_list, nonCFM_port_count_list = get_connect_switch(switch_uuid)

    # Switch List in Pickle
    #Do some serialization using pickle module with switch on nonCFM
    #This will create a tmp file with all switches and data 
    pickle_out = open("noncfm_switch_list.tmp", "wb")
    pickle.dump(switch_list, pickle_out)
    pickle_out.close()
    
    strip_switch_data(switch_list)
    new_dict = strip_switch_data(switch_list)
    order_dict_on_label(new_dict)
    connect_ports = order_dict_on_label(new_dict)
    #print connect_ports['rupert'][0]['uuid'] # this will get you port label 1, UUID for rupert as stored in Connect.
   

#################################################################################################
#### Now do the CFM Portion ########################################################################
#################################################################################################

    #The switches have been ONIED to 5.0 and px-setup run on each switch, so that they have the correct IP and hostname, that matches the 4.1
    # configuration.


    #Get the switch IP address, name and description to pass for creating fabric function
    
    get_fabric(fab_response)
    fabric_name, fabric_description =  get_fabric(fab_response)
    print "The fabric Name is: " + fabric_name
    print "The fabric description is: " + fabric_description
    switch_for_fab = get_switch_ip(sw_response)[0] # Get the first IP address for a switch
    print "The switch being used for CFM fabric discover is: " + switch_for_fab
    
    
    #TODO Uncomment the below two lines if you need to create a fabric->>>>>>>>>>>
    #print add_fabric(CFM_session, switch_for_fab, fabric_name, fabric_description) # Create the fabric and return 'result'
    #time.sleep(60) # sleep for 60 seconds to allow for fabric creation.
    #TODO Remove above comments if you need to create the fabric- as first time use.
    
    #TODO - Add a check in for ensuring Fabric is in a good state and ready for POSTING
    

    # At this point the fabric should have been created and all switches discovered.

    # pull back the switches names,UUID, MAC and IP address from CFM
    print "The switch names from Connect: " + str(get_switch_name(sw_response))
    print "The switch names from CFM: " + str(get_switch_name(cfm_switch_response))
    print "Switch UUIDs from CFM: "
    cfm_switch_uuid = get_switch_uuid(cfm_switch_response)
    cfm_switch_list, cfm_port_count_list  = get_CFM_switch(cfm_switch_uuid)
    cfm_new_dict = strip_switch_data(cfm_switch_list)
    order_dict_on_label(cfm_new_dict)
    cfm_ports = order_dict_on_label(cfm_new_dict)
    print "The port count list for Connect: "
    print nonCFM_port_count_list
    print "\n"
    print "The  port count list for CFM: "
    print cfm_port_count_list
    compare_port_counts(nonCFM_port_count_list, cfm_port_count_list) # make sure the number of ports cfm and connect retrieve match count

    switch_name = get_switch_name(cfm_switch_response)
    print set_cfm_port_info(CFM_session,cfm_ports,connect_ports,switch_name,cfm_port_count_list) 
        


if __name__ == '__main__':
    main()

