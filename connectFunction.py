#!/usr/bin/env python

from netmiko import ConnectHandler
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_list = ['172.16.0.1', '172.16.0.3', '172.16.0.5']
junos_list = ['172.16.0.4']
with open('junos_commands_file') as f:
    junos_commands = f.read().splitlines()

def connector(device,vendor,commands):
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

for device in junos_list:
    connector(device,'juniper_junos',junos_commands)
