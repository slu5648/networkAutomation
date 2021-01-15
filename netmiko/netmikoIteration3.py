#!/usr/bin/env python

from netmiko import ConnectHandler
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
    connector(device, 'cisco_ios', ios_commands)

for device in junos_devices:
    connector(device, 'juniper_junos', junos_commands)
