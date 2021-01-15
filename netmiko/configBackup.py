#!/usr/bin/env python

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from simplecrypt import decrypt
from time import time
import json
import getpass

'''
This function is used to read the encrypted credentials file
'''
def read_encrypted_creds(encryptedFile, key):
    print('\n... getting credentials ...\n')
    with open(encryptedFile, 'rb') as device_creds_file:
        device_creds_json = decrypt(key, device_creds_file.read())
        device_creds = json.loads(device_creds_json.decode('utf-8'))
        return device_creds

'''
This function is used to build connections, discover the OS, and backup the config to it's working directory
'''
def connector(device_ip):
    print('Connecting to ' + device_ip)
    device = {
        'device_type': 'terminal_server',
        'ip': device_ip,
        'username': device_creds['username'],
        'password': device_creds['password']
    }
    discovery_connect = ConnectHandler(**device)
    for os in os_list:
        output = discovery_connect.send_command('show version')
        commands = None
        software_vendor = 0
        software_vendor = output.find(os)
        if software_vendor > 0:
            print('Software is ' + os)
            break
    if os == 'JUNOS':
        device['device_type'] = 'juniper_junos'
        command = 'show configuration'
    elif os == 'IOS':
        device['device_type'] = 'cisco_ios'
        command = 'show running-config'

    if command is None:
        print('Unknown Operating System, aborting')
    else:
        print('Running {} commands'.format(os))
        session = ConnectHandler(**device)
        output = session.send_command(command)
        config_filename = 'config-' + device_ip
        print('--- Writing Configuration: ', config_filename)
        with open(config_filename, 'w') as config_out:
            config_out.write(output)
        session.disconnect()
        return

'''
Get the user input to fill necessary variables
'''
encryptedFile = input('File containing the encrypted credentials: ')
key = getpass.getpass('Encryption Key: ')

'''
Open up the various files we will need to for the connector function to perform it's work
'''

with open('networkDevices') as f:
    network_devices = f.read().splitlines()

with open('network_os') as f:
    os_list = f.read().splitlines()

'''
Worker job
'''
device_creds = read_encrypted_creds(encryptedFile, key)
print('Trying username ' + device_creds['username'] + ' with a password of ' + device_creds['password'])

starting_time = time()

for device_ip in network_devices:
    try:
        connector(device_ip)
    except AuthenticationException:
        print('Authentication failure: ' + device_ip)
        continue
    except NetMikoTimeoutException:
        print('Timeout to device: ' + device_ip)
        continue
    except EOFError:
        print("End of file while attempting device " + device_ip)
        continue
    except SSHException:
        print('SSH Issue.  Are you sure SSH is enabled? ' + device_ip)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue

print('\nTotal time for this job was ', time()-starting_time)
