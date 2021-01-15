#!/usr/bin/env python

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
import getpass


def connector(device, vendor, commands):
    print('Connecting to ' + device)
    device = {
        'device_type': vendor,
        'ip': device,
        'username': user,
        'password': password
    }
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(commands)
    print(output)

user = input('Username: ')
password = getpass.getpass()

with open('ciscoDevices') as f:
    ios_devices = f.read().splitlines()
with open('junosDevices') as f:
    junos_devices = f.read().splitlines()
with open('ios_commands_file') as f:
    ios_commands = f.read().splitlines()
with open('junos_commands_file') as f:
    junos_commands = f.read().splitlines()

for device in ios_devices:
    try:
        connector(device, 'cisco_ios', ios_commands)
    except AuthenticationException:
        print('Authentication failure: ' + device)
        continue
    except NetMikoTimeoutException:
        print('Timeout to device: ' + device)
        continue
    except EOFError:
        print("End of file while attempting device " + device)
        continue
    except SSHException:
        print('SSH Issue.  Are you sure SSH is enabled? ' + device)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue

for device in junos_devices:
    try:
        connector(device, 'juniper_junos', junos_commands)
    except AuthenticationException:
        print('Authentication failure: ' + device)
        continue
    except NetMikoTimeoutException:
        print('Timeout to device: ' + device)
        continue
    except EOFError:
        print("End of file while attempting device " + device)
        continue
    except SSHException:
        print('SSH Issue.  Are you sure SSH is enabled? ' + device)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue
