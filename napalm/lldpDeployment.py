import csv
import json
from getpass import getpass
from napalm import get_network_driver

username = input('Username: ')
password = getpass()

iosDriver = get_network_driver('ios')
junosDriver = get_network_driver('junos')
nxosDriver = get_network_driver('nxos')

def main(device):
    device.open()
    print("Getting facts from " + line[1] + "\n\n")
    lldp_neighbors = device.get_lldp_neighbors()
    lldp_detail = device.get_lldp_neighbors_detail()
    for line in lldp_neighbors:
        if line != 'GigabitEthernet0/0':
            local_interface = line
            remote_device = lldp_neighbors[line][0]['hostname']
            config_commands = local_interface + '\ndescription' + remote_device

    device.close()

with open('deviceInventory') as inventoryFile:
    csv_reader = csv.reader(inventoryFile)
    for line in csv_reader:
        if line[2] == 'IOSv':
            device = iosDriver(line[1], username, password)
            main(device)
