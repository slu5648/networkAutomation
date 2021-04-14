#!/usr/bin/env python

import getpass
import threading
from time import time
from netmiko import ConnectHandler
from multiprocessing.dummy import Pool as ThreadPool
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

with open('networkDevices') as f:
    network_devices = f.read().splitlines()

with open('network_os') as f:
    os_list = f.read().splitlines()

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
------------Main: Get Configuration
'''

user = input('Username: ')
password = getpass.getpass()
command_set = input('Command Set to apply: ')

ios_command_set = 'ios-' + command_set
junos_command_set = 'junos-' + command_set

with open('ios_command_set') as f:
    ios_commands = f.read().splitlines()

with open('junos_command_set') as f:
    junos_commands = f.read().splitlines()

num_threads_str = input('\nNumber of threads (2): ') or '2'
num_threads = int(num_threads_str)

config_threads_list = []
for device_ip in network_devices:
    config_threads_list.append(device_ip)

print('\n---- Creating Thread Pools ----\n')
threads = ThreadPool(num_threads)
results = threads.map(connector, config_threads_list)

threads.close()
threads.join()

