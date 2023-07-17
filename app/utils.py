import re


def format_mac_addr(mac_addr: str):
    '''Change format of mac_addr to uppercase and using '-' as separator
    '''
    # Change mac_addr to uppercase
    mac_addr = mac_addr.upper()

    # Change separator from ':' to '-'
    mac_addr = mac_addr.replace(':', '-')

    return mac_addr


def validate_mac_addr(mac_addr: str):
    '''Validates mac_addr is not empty.
    Validates mac_addr is proper format using regex.
    '''
    # Assert mac_addr is not empty. 
    if mac_addr == '':
        raise AssertionError ('Exception: MAC Address cannot be empty.')
    else: # MAC Address is not empty
        # Assert mac_addr is valid format.
        if re.match('([0-9A-F]{2}[-:]){5}([0-9A-F]{2})$', mac_addr.upper()):
            return True
        else:
            raise AssertionError ('Exception: MAC Address does not contain separators.')


def validate_vlan_id(vlan_id):
    '''Validates vlan_id is not empty.
    Validates vlan_id is proper format using regex.
    '''
    # Assert vlan_id is not empty.
    if vlan_id == '':
        raise AssertionError ('Exception: VLAN ID cannot be empty.')
    else: 
        # Assert vlan_id is of type int.      
        try:
            vlan_id = int(vlan_id)
        except ValueError:
            raise AssertionError ('Exception: VLAN ID is not of type int.')


def parse_values(values: str):
    '''Parses row_id, mac_addr and vlan_id from String values
    '''
    list_values = values.split(", ")
    row_id = list_values[0][1:]
    mac_addr = list_values[1][1:-1]
    vlan_id = list_values[2][:-1]

    return row_id, mac_addr, vlan_id
