from netmiko import ConnectHandler

#list = open('myswitches')
#vlanDict: Dict[int, Any] = {}
#with open("vlanDictionary") as dictFile:
#    for line in dictFile:
#        (key, val) = line.strip().split(':')
#        vlanDict[int(key)] = val
#for IP in list:
#    IP = IP.strip()
d1 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.0.1',
    'username': 'jason',
    'password': 'copas'
}

s1 = {
    'device_type': "cisco_ios",
    'ip': "172.16.0.2",
    'username': 'jason',
    'password': 'copas'
}

s2 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.0.3',
    'username': 'jason',
    'password': 'copas'
}

all_devices = [d1, s1, s2]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    for n in range (2,21):
        print ("creating vlan" + str(n))
        config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
        output = net_connect.send_config_set(config_commands)
        print(output)

#config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.0']
#output = net_connect.send_config_set(config_commands)
#print(output)

#for IP in list:
#    print("Creating VLAN " + str(n))
#    config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
#    output = net_connect.send_config_set(config_commands)
#    print(output)
#
#
#for IP in list:
#    IP = IP.strip()
#    print("Configuring Switch " + (IP))
#    HOST = IP
#    tn = telnetlib.Telnet(HOST)
#    tn.read_until(b"Username: ")
#    tn.write(user.encode('ascii') + b"\n")
#    if password:
#        tn.read_until(b"Password: ")
#        tn.write(password.encode('ascii') + b"\n")
#    tn.write(b"configure terminal\n")
#    for key, value in vlanDict.items():
#        tn.write(b"vlan " + str(key).encode('ascii') + b"\n")
#        tn.write(b"name " + vlanDict[value].encode('ascii') + b"\n")
#    tn.write(b"end\n")
#    tn.write(b"exit\n")
#    print(tn.read_all().decode('ascii'))
