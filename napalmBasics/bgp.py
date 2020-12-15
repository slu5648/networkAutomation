import json
from napalm import get_network_driver
iosDriver = get_network_driver('ios')
junosDriver = get_network_driver('junos')
nxosDriver = get_network_driver('nxos')

iosv = iosDriver('172.16.0.5', 'jason', 'P@ssword')
iosv.open()
ios_output = iosv.get_facts()
ios_bgp = iosv.get_bgp_neighbors()
print('Connecting to iosv-L3')
print(json.dumps(ios_output, indent=4))
print(json.dumps(ios_bgp, indent=4))

vsrx = junosDriver('172.16.0.4', 'jason', 'P@ssword')
vsrx.open()
vsrx_output = vsrx.get_facts()
vsrx_bgp = vsrx.get_bgp_neighbors()
print('Connecting to vSRX')
print(json.dumps(vsrx_output, indent=4))
print(json.dumps(vsrx_bgp, indent=4))

#nxos = nxosDriver('172.16.0.2', 'jason', 'P@ssword')
#nxos.open()
#nxos_output = nxos.get_facts()
#nxos_bgp = nxos.get_bgp_neighbors()
#print('Connecting to Nexus')
#print(json.dumps(vsrx_output, indent=4))
#print(json.dumps(vsrx_bgp, indent=4))
