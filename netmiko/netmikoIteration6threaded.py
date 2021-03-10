#!/usr/bin/env python

import getpass
import threading
from time import time
from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

with open('networkDevices') as f:
    network_devices = f.read().splitlines()

with open('network_os') as f:
    os_list = f.read().splitlines()

with open('ios_commands_file') as f:
    ios_commands = f.read().splitlines()

with open('junos_commands_file') as f:
    junos_commands = f.read().splitlines()

def connector(device_ip):
    print('Connecting to ' + device_ip)
    device = {
        'device_type': 'terminal_server',
        'ip': device_ip,
        'username': user,
        'password': password
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
        commands = junos_commands
    elif os == 'IOS':
        device['device_type'] = 'cisco_ios'
        commands = ios_commands
    if commands is None:
        print('Unknown Operating System, aborting')
    else:
        print('Running {} commands'.format(os))
        config_connect = ConnectHandler(**device)
        output = config_connect.send_config_set(commands)
        print(output)

'''
Working Configuration
'''

user = input('Username: ')
password = getpass.getpass()

starting_time = time()

config_threads_list = []
for device_ip in network_devices:
    print ('Creating thread for: ', device_ip)
    config_threads_list.append( threading.Thread( target=connector, args=([device_ip])))

print ('\n---- Begin get config threading ----\n')
for config_thread in config_threads_list:
    config_thread.start()

for config_thread in config_threads_list:
    config_thread.join()

stopping_time = time()

print ('\n Elapsed Time: \n', starting_time - stopping_time)

'''    
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
'''
