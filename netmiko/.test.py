#!/usr/bin/env python

from netmiko import ConnectHandler
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_list = ['172.16.0.1', '172.16.0.3', '172.16.0.5']
junos_list = ['172.16.0.4']

def connector(vendor):
    print('Connecting to ' + device)
    device_ip = device
    device = {
        'device_type': vendor,
        'ip': device_ip,
        'username': user,
       'password': password
    }
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(vendor + '_commands')
    print(output)

for ip in junos_list:
    connector(juniper_junos)
