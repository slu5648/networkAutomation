import getpass
from netmiko import ConnectHandler

user = input("username: ")
password = getpass.getpass()
with open('ciscoSwitches') as ciscoIPs:
    lines = ciscoIPs.read().splitlines()
for line in lines:
    device = {
        'device_type': 'cisco_ios',
        'ip': line,
        'username': user,
        'password': password
    }
    with open('iosv_l2_cisco_design') as config:
        edit = config.read().splitlines()
        net_connect = ConnectHandler(**device)
        output = net_connect.send_config_set(edit)
        print(output)
