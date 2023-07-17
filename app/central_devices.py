# Import Aruba Central Base
from pycentral.base import ArubaCentralBase

# Import credentials
from creds_central import central_info


# Create an instance of ArubaCentralBase 
ssl_verify = True
central = ArubaCentralBase(central_info=central_info,
                           token_store=None,
                           ssl_verify=ssl_verify)


def get_clients():
    '''Get clients from Aruba Central and return tuple of headings and clients.
    '''
    # # Declare headings to display in table
    # headings = ('Client Type', 'Connected Device Type', 'Manufacturer', 'MAC', 'OS Type', 'Group Name', 'Associated Device Name', 'Interface Port', 'VLAN')

    # Declare headings to display in table
    headings = ('Client Type', 'Connected Device Type', 'Manufacturer', 'MAC', 'OS Type', 'Group Name', 'Associated Device Name', 'VLAN')


    # Get wired clients from API
    resp_wired = central.command('GET', '/monitoring/v1/clients/wired')
    resp_wired = resp_wired['msg']['clients']

    # Get wireless clients from API
    resp_wireless = central.command('GET', '/monitoring/v1/clients/wireless')
    resp_wireless = resp_wireless['msg']['clients']

    # Combine wireless & wired clients
    resp_clients = resp_wired + resp_wireless

    # Declare empty list for clients
    return_clients = []

    # Declare row counter
    row_counter = 0

    # # Get attributes matching headings for every client and save in list
    # for client in resp_clients:
    #     return_clients.append((row_counter, client['client_type'], client['connected_device_type'], client['manufacturer'], 
    #                            client['macaddr'], client['os_type'], client['group_name'], client['associated_device_name'], 
    #                            client['interface_port'], client['vlan']))
    #     row_counter = row_counter + 1

    # Get attributes matching headings for every client and save in list
    for client in resp_clients:
        return_clients.append((row_counter, client['client_type'], client['connected_device_type'], client['manufacturer'], 
                               client['macaddr'], client['os_type'], client['group_name'], client['associated_device_name'], client['vlan']))
        row_counter = row_counter + 1

    # Return tuple of headings and clients
    return headings, return_clients
