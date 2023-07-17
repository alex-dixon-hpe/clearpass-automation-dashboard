# Imports from flask
from flask import Flask, render_template, request, flash, url_for, send_from_directory

# Import needed to show /favicon.ico
import os

# Declare subdirectory 'app'
import sys
sys.path.append('app')

# Import files from subdirectory 'app'
from creds_cppm import cppm_info as creds
from change_vlan import change_vlan_id
from central_devices import *
from utils import format_mac_addr, parse_values


# Flask specific settings
# Create flask app instance and set template folder
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
# Import config file
app.config.from_pyfile('config.py')
# Read access token from creds
access_token = creds['access_token']


# Define routes
@app.route('/')
def index():
    '''Renders homepage on route '/'
    '''
    # Render index.html on route '/'
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    '''Renders Aruba favicon on route '/favicon.ico'
    '''
    # Send favicon.ico when route '/favicon.ico' is accessed
    return app.send_static_file('favicon.ico')


@app.route('/change-vlan', methods=['GET', 'POST'])
def change_vlan():
    '''Renders change-vlan page on route '/change_vlan'
    If request method is 'POST', MAC address and VLAN ID are retrieved from form and 
        passed to template.
    Else template is rendered without variables.
    '''
    if request.method == 'POST':
        # If case is when request triggered by 'Change VLAN' button
        if request.form.get('edit'):
            # Retrieve values from 'edit' form
            values = request.form.get('edit')

            # Parse out true values from 'edit' form data
            row_id, mac_addr, vlan_id = parse_values(values)

            # Render template with mac_addr and vlan_id already filled
            return render_template('change-vlan.html', value_mac_addr=mac_addr, value_vlan_id=vlan_id)
        
        # Else case is when request triggered by manually inputting values
        else:
            # Retrieve MAC address and VLAN ID from form
            mac_addr = request.form['mac-addr']
            vlan_id = request.form['vlan-id']

            # Ensure mac_addr is correct format
            mac_addr = format_mac_addr(mac_addr)

            # Change VLAN ID and save response
            response = change_vlan_id(mac_addr=mac_addr, vlan_id=vlan_id)

            # Render template
            return render_template('change-vlan.html')
    
    # Else case is when '/change-vlan' is accessed
    else:
        return render_template('change-vlan.html')


@app.route('/central-devices')
def central_devices():
    '''Renders central-devices page on route '/central-devices'
    Shows wireless/wired devices from Central. 
    '''
    # Get and separate out headings and clients
    headings, clients = get_clients()

    # Render template and pass headings and clients
    return render_template('central-devices.html', headings=headings , data=clients)


if __name__ == '__main__':
    app.run(debug=True)
