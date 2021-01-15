#!/usr/bin/env python

from netmiko import ConnectHandler
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_devices = ['172.16.0.1', '172.16.0.3', '172.16.0.5']
junos_devices = ['172.16.0.4']


with open('ios_commands_file') as f:
    ios_commands = f.read().splitlines()
with open('junos_commands_file') as f:
    junos_commands = f.read().splitlines()

for device in ios_devices:
    print('Connecting to ' + device)
    device_ip = device
    device = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': user,
        'password': password
    }
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(ios_commands)
    print(output)

for device in junos_devices:
    print('Connecting to ' + device)
    device_ip = device
    device = {
        'device_type': 'juniper_junos',
        'ip': device_ip,
        'username': user,
        'password': password
    }
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(junos_commands)
    print(output)
