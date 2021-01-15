#!/usr/bin/env python

from netmiko import ConnectHandler
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_list = ['172.16.0.1', '172.16.0.3', '172.16.0.5']
junos_list = ['172.16.0.4']

for ip in junos_list:
    junosDevice = {
        'device_type': 'juniper_junos',
        'ip': ip,
        'username': user,
        'password': password
    }
    print('Connecting to ' + ip)
    net_connect = ConnectHandler(**junosDevice)
    output = net_connect.send_command('show interface terse')
    print(output)
