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

with open('iosv_l2_cisco_design') as f:
    lines = f.read().splitlines()
print(lines)

all_devices = [d1, s1, s2]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_config_set(lines)
    print(output)
