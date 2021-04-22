import csv
import time
from getpass import getpass
from netmiko import ConnectHandler
from napalm import get_network_driver

username = input('Username: ')
password = getpass()

iosDriver = get_network_driver('ios')
junosDriver = get_network_driver('junos')
nxosDriver = get_network_driver('nxos')


def main(device):
    device.open()
    device.load_merge_candidate(config='lldp run')
    lldp_diffs = device.compare_config()
    if len(lldp_diffs) > 0:
        print('lldp not enabled, turning on lldp and waiting 30 seconds to form neighborships to form')
        device.commit_config()
        time.sleep(30)
    else:
        device.discard_config()
    lldp_neighbors = device.get_lldp_neighbors()
    has_neighbors = bool(lldp_neighbors)
    interfaces = device.get_interfaces()
    if has_neighbors == True:
        for line in lldp_neighbors:
            if line != 'GigabitEthernet0/0':
                local_interface = line
                remote_device = lldp_neighbors[line][0]['hostname']
                if interfaces[line]['description'] == remote_device:
                    print(line + ' description is correct')
                else:
                    int_desc = 'interface ' + local_interface + '\ndescription ' + remote_device
                    device.load_merge_candidate(config=int_desc)
                    desc_diffs = device.compare_config()
                    if len(desc_diffs) > 0:
                        print('Correcting missing or incorrect description on ' + line)
                        print(desc_diffs)
                        device.commit_config()
    else:
        print('Did not find any neighbors')
    device.close()


def connector(command):
    device = {
        'device_type': 'cisco_ios',
        'ip': deviceIP,
        'username': username,
        'password': password
    }
    config_connect = ConnectHandler(**device)
    config_connect.send_config_set(command)


with open('deviceInventory') as inventoryFile:
    csv_reader = csv.reader(inventoryFile)
    for line in csv_reader:
        deviceName = line[0]
        deviceIP = line[1]
        if line[2] == 'IOSv':
            device = iosDriver(deviceIP, username, password, optional_args={'inline_transfer': 'True'})
            enable_scp = 'ip scp server enable'
            print('\nConnecting to ' + deviceName)
            connector(enable_scp)
            main(device)
