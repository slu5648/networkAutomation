import json
import csv
from getpass import getpass
from napalm import get_network_driver

username = input('Username: ')
password = getpass()

iosDriver = get_network_driver('ios')
junosDriver = get_network_driver('junos')
nxosDriver = get_network_driver('nxos')

with open('deviceInventory') as inventoryFile:
    csv_reader = csv.reader(inventoryFile)
    for line in csv_reader:
        if line[2] == 'IOSv':
            ios = iosDriver(line[1], username, password)
            ios.open()
            ios_facts = ios.get_facts()
            print(line[1] + ' facts')
            print(json.dumps(ios_facts, indent=4))
        if line[2] == 'Juniper':
            junos = junosDriver(line[1], username, password)
            junos.open()
            junos_facts = junos.get_facts()
            print(line[1] + ' facts')
            print(json.dumps(junos_facts, indent=4))
