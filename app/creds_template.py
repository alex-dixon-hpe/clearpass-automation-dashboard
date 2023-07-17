''' Configuration of ClearPass API credentials

You MUST configure the 'host' member variable and one of the following for authorization:

- access_token (if you already performed OAuth2 authentication)
- client_id, client_secret (implies grant_type=client_credentials)
- client_id, username, password (implies grant_type=password, public client)
- client_id, client_secret, username, password (implies grant_type=password)

Copy the following block into a new file and name it 'creds_cppm.py'. Then configure the following variables as required.
'''
cppm_info = {
    'username': '',
    'password': '',
    'client_id': '',
    'client_secret': '',
    'access_token': '',
    'host': ''
}

''' Configuration of Central API credentials

Copy the following block into a new file and name it 'creds_central.py'. Then configure the following variables as required.
'''
central_info = {
            "client_id": "",
            "client_secret": "",
            "customer_id": "",
            "base_url": "",
        }
