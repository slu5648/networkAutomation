import getpass
from netmiko import ConnectHandler

user = input("username: ")
password = getpass.getpass()

with open('ciscoSwitches') as ciscoIPs:
    ciscoDevs = ciscoIPs.read().splitlines()
for ciscoIP in ciscoDevs:
    ciscoDev = {
        'device_type': 'cisco_ios',
        'ip': ciscoIP,
        'username': user,
        'password': password
    }
    with open('ios_python.config') as ciscoConfig:
        ciscoEdit = ciscoConfig.read().splitlines()
        net_connect = ConnectHandler(**ciscoDev)
        output = net_connect.send_config_set(ciscoEdit)
        print(output)

#with open('junosDevices') as junosIPs:
#    junosDevs = junosIPs.read().splitlines()
#for junosIP in junosDevs:
#    junosDev = {
#        'device_type': 'juniper',
#        'ip': junosIP,
#        'username': user,
#        'password': password
#    }
#    with open('vsrx_python.config') as juniperConfig:
#        juniperEdit = juniperConfig.read().splitlines()
#        net_connect = ConnectHandler(**junosDev)
#        output = net_connect.send_config_set(juniperEdit)
#        print(output)
