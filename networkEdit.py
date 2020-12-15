import getpass
from netmiko import ConnectHandler

user = input("username: ")
password = getpass.getpass()

with open('ciscoAccess.ip') as accessIPs:
    accessDevs = accessIPs.read().splitlines()
with open('ciscoDist.ip') as distIPs:
    distDevs = distIPs.read().splitlines()
allDevs = accessDevs + distDevs

for eachIP in allDevs:
    eachDev = {
        'device_type': 'cisco_ios',
        'ip': eachIP,
        'username': user,
        'password': password
    }
    with open('ciscoCore.config') as coreConfig:
        coreEdit = coreConfig.read().splitlines()
        net_connect = ConnectHandler(**eachDev)
        output = net_connect.send_config_set(coreEdit)
        print(output)
for accessIP in accessDevs:
    accessDev = {
        'device_type': 'cisco_ios',
        'ip': accessIP,
        'username': user,
        'password': password
    }
    with open('ciscoAccess.config') as accessConfig:
        accessEdit = accessConfig.read().splitlines()
        net_connect = ConnectHandler(**accessDev)
        output = net_connect.send_config_set(accessEdit)
        print(output)

for distIP in distDevs:
    distDev = {
        'device_type': 'cisco_ios',
        'ip': distIP,
        'username': user,
        'password': password
    }
    with open('ciscoDist.config') as distConfig:
        distEdit = distConfig.read().splitlines()
        net_connect = ConnectHandler(**distDev)
        output = net_connect.send_config_set(distEdit)
        print(output)
