import getpass
from netmiko import ConnectHandler

user = input("username: ")
password = getpass.getpass()

d1 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.0.1',
    'username': user,
    'password': password
}

s1 = {
    'device_type': "cisco_ios",
    'ip': "172.16.0.2",
    'username': user,
    'password': password
}

s2 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.0.3',
    'username': user,
    'password': password
}

all_devices = [d1, s1, s2]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    for n in range (2,21):
        print ("creating vlan" + str(n))
        config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
        output = net_connect.send_config_set(config_commands)
        print(output)