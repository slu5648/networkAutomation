import os
import csv
from datetime import datetime, date, time
from getpass import getpass
from napalm import get_network_driver

username = input('Username: ')
password = getpass()

iosDriver = get_network_driver('ios')
junosDriver = get_network_driver('junos')
nxosDriver = get_network_driver('nxos')

def main(device):
    device.open()
    device_facts = device.get_lldp_neighbors()
    print("Getting facts from " + line[1] + "\n\n")
    device.close()

with open('deviceInventory') as inventoryFile:
    csv_reader = csv.reader(inventoryFile)
    for line in csv_reader:
        if line[2] == 'IOSv':
            device = iosDriver(line[1], username, password)
            main(device)
        if line[2] == 'Juniper':
            device = junosDriver(line[1], username, password)
            main(device)
            main(driver)
