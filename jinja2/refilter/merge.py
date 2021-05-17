from jnpr.junos import Device
from jnpr.junos.utils.config import Config
#import jxmlease
import getpass
import yaml
import jinja2

# Interactive Prompts
device_name = input('Device to connect to: ')
user_name = input('SSH Username: ')
password = getpass.getpass()

# Builds the objects that we will be calling throughout the script
dev = Device(device_name, user=user_name, passwd=password)
templateLoader = jinja2.FileSystemLoader(searchpath="../templates/")
templateEnv = jinja2.Environment(loader=templateLoader)

# Retrieve BGP information from the device
dev.open()
xml_filter = '<routing-instances><instance><protocols><bgp><group><neighbor/></group></bgp></protocols></instance></routing-instances>'
bgp_config = dev.rpc.get_config(filter_xml=xml_filter, options={'format':'json'})
dev.close()

# Identifiy what neighbors are configured for the device
bgp_neighbors = bgp_config['configuration']['routing-instances']['instance'][0]['protocols']['bgp']['group'][0]['neighbor'][0]['name']
neighbor_list = []
for line in bgp_neighbors:
    neighbor_list.append(line['name'])
neighbor_dict = {}
neighbor_dict['neighbors'] = neighbor_list

# Start building the yaml file to fill out the refilter jinja2 template
vars_template = templateEnv.get_template('refilterVars.yml')
vars_yaml = vars_template.render(neighbor_dict)
with open(device_name + '.yml', 'w') as f:
    print(vars_yaml, file=f)

# Start building the configuration for the device
config_vars = yaml.load(open(device_name + '.yml').read(), Loader=yaml.FullLoader)
conf_template = templateEnv.get_template('refilter.conf')
config = conf_template.render(config_vars)
config_path = device_name + '.conf'
with open(config_path, 'w') as f:
    print(config, file=f)


with Config(dev.open(), mode='exclusive') as cu:
    cu.load(path=config_path, format='text', merge=True)
    cu.pdiff()
    cu.commit(confirm=2)


dev.close()

with Config(dev.open(), mode='exclusive') as cu:
    cu.commit_check()


dev.close()
