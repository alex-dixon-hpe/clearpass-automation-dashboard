# External imports
from flask import jsonify, flash

# Internal imports
from creds_cppm import cppm_info as creds
from clearpass import api
from utils import *


# Read host and access token from creds_cppm
host = creds['host']
access_token = creds['access_token']

# Create an api.Client object
client = api.Client(host=host, access_token=access_token)


def change_vlan_id(mac_addr, vlan_id):
    '''Procedure to change VLAN ID of specified MAC Address. 
    Checks validity of mac_addr and vlan_id and calls individual procedural functions.
    '''
    # Validate mac_addr
    try:
        validate_mac_addr(mac_addr)
    except AssertionError as e:
        flash(e.args[0], 'danger')
        return e.args[0]

    # Validate vlan_id
    try:
        validate_vlan_id(vlan_id)
    except AssertionError as e:
        flash(e.args[0], 'danger')
        return e.args[0]    

    # Change vlan_id
    resp_change_vlan_id = patch_change_vlan_id(mac_addr=mac_addr, vlan_id=vlan_id)
    
    # Get session_id for mac_addr
    try:
        session_id = get_session_id_for_mac(mac_addr=mac_addr)
    except AssertionError as e:
        flash(e.args[0], 'danger')
        return e.args[0]

    # Reauthorize session
    resp_reauth = post_reauthorize_session(session_id)

    # Add responses from different procedure calls to list
    resp = []
    resp.append(resp_change_vlan_id)
    resp.append(session_id)
    resp.append(resp_reauth)

    return resp


def get_endpoint_information(mac_addr):
    '''Retrieves endpoint information for MAC address.
    
    :r_type: response
    '''
    # Construct url with MAC address
    url = '/endpoint/mac-address/' + mac_addr

    # Try api call and throw exception for errors
    try:
        response = client.get(url=url)
    except api.Error as e:
        flash('Internal Exception: API exception, Status code: ' + str(e.code), 'danger')
        return 'Internal Exception: API exception, Status code: ' + str(e.code)
    except api.ConfigurationException as conf_e:
        flash('Internal Exception: API configuration exception', 'danger')
        return 'Internal Exception: API configuration exception'

    return response


def patch_change_vlan_id(mac_addr, vlan_id):
    '''Changes VLAN ID of MAC address

    :r_type: response
    '''
    # Construct url with MAC address
    url = '/endpoint/mac-address/' + mac_addr
    
    # Construct body with VLAN ID
    body = {'attributes': {'vlan': vlan_id}}

    # Try api call and throw exception for errors
    try:
        response = client.patch(url=url, body=body)
    except api.Error as e:
        flash('Internal Exception: API exception, Status code: ' + str(e.code), 'danger')
        return 'Internal Exception: API exception, Details: ' + str(e.details) + ' Status code: ' + str(e.code)
    except api.ConfigurationException as conf_e:
        flash('Internal Exception: API configuration exception', 'danger')
        return 'Internal Exception: API configuration exception'
    
    flash('VLAN ID has been changed.', 'success')

    return response


def get_session_id_for_mac(mac_addr):
    '''Retrieves session ID for client where 'mac_address' == mac_addr and 'state' == 'active'
    '''
    # Construct url
    url = '/session'

    # Try api call and throw exception for errors
    try:
        response = client.get(url=url)
    except api.Error as e:
        flash('Internal Exception: API exception, Status code: ' + str(e.code), 'danger')
        return 'Internal Exception: API exception, Details: ' + str(e.details) + ' Status code: ' + str(e.code)
    except api.ConfigurationException as conf_e:
        flash('Internal Exception: API configuration exception', 'danger')
        return 'Internal Exception: API configuration exception'

    # Extract items, get length of item list
    items = response['_embedded']
    length = len(items['items'])

    # Loop through response items
    for i in range(length - 1):
        # If MAC of item matches mac_addr and state of item is active return session id of item
        if items['items'][i]['mac_address'] == mac_addr and items['items'][i]['state'] == 'active':
            return items['items'][i]['id']
    
    # TODO: Implement else case, catch case that no match is found
    

def post_reauthorize_session(session_id):
    '''Reauthorizes session of client with session_id variable
    '''
    # Construct url with session ID
    url = '/session/' + str(session_id) + '/reauthorize'

    # Body for reauthorization
    body = {"confirm_reauthorize": True, "reauthorize_profile": "[AOS-CX - Bounce Switch Port]"}

    # Try api call and throw exception for errors
    try:
        response = client.post(url=url, body=body)
    except api.Error as e:
        flash('Internal Exception: API exception, Status code: ' + str(e.code), 'danger')
        return 'Internal Exception: API exception, Details: ' + str(e.details) + ' Status code: ' + str(e.code)
    except api.ConfigurationException as conf_e:
        flash('Internal Exception: API exception', 'danger')
        return 'Internal Exception: API configuration exception'

    flash('Session has been reauthorized.', 'success')
    
    return response
