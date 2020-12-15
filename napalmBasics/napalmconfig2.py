import json
from napalm import get_network_driver
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_list = ['172.16.0.1', '172.16.0.3', '172.16.0.5']
junos_list = ['172.16.0.4']

for ip in ios_list:
    iosDriver = get_network_driver('ios')
    iosV = iosDriver(ip, user, password)
    iosV.open()
    print('Accessing ' + str(ip))
    iosV.load_merge_candidate(filename='ACL1.cfg')
    diffs = iosV.compare_config()
    if len(diffs) > 0:
        print(diffs)
        iosV.commit_config()
    else:
        print('No changes required')
        iosV.discard_config()
    iosV.close()
