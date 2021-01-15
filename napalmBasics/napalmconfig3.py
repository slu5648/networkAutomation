import json
from napalm import get_network_driver
import getpass

user = input('Username: ')
password = getpass.getpass()
ios_list = ['172.16.0.3', '172.16.0.5']

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
        print('No ACL changes required')
        iosV.discard_config()
    iosV.load_merge_candidate(filename=ospf1.cfg)
    diffs = iosV.compare_config()
    if len(diffs) > 0:
        print(diffs)
        iosV.commit_config()
    else:
        print('No OSPF changes required')
        iosV.discard_config()
    iosV.close()
