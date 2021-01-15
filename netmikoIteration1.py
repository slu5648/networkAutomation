#!/usr/bin/env python

from netmiko import ConnectHandler
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_list = ['172.16.0.1', '172.16.0.3', '172.16.0.5']

for ip in ios_list:
    iosDevice = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': user,
        'password': password
    }
    print('Connecting to ' + ip)
    net_connect = ConnectHandler(**iosDevice)
    output = net_connect.send_command('show ip int brief')
    print(output)
