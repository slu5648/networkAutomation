import json
from napalm import get_network_driver
driver = get_network_driver('junos')
junos = driver('172.16.0.5', 'jason', 'P@ssword')
junos.open()

bgp_neighbors = junos.get_bgp_neighbors()
print(json.dumps(bgp_neighbors, indent=4))

junos.close()
