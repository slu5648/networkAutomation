import getpass
import telnetlib
from typing import Dict, Any

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

list = open('myswitches')
vlanDict: Dict[int, Any] = {}
with open("vlanDictionary") as dictFile:
    for line in dictFile:
        (key, val) = line.strip().split(':')
        vlanDict[int(key)] = val
for IP in list:
    IP = IP.strip()
    print("Configuring Switch " + (IP))
    HOST = IP
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b"configure terminal\n")
    for key, value in vlanDict.items():
        tn.write(b"vlan " + str(key).encode('ascii') + b"\n")
        tn.write(b"name " + vlanDict[value].encode('ascii') + b"\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))