import yaml
import jinja2

# Interactive Prompts and build the dictionary to build the yaml file
vars_dict = {}
vars_dict['site_name'] = input('Site Name: ')
vars_dict['device_name'] = input('Device Name: ')
device_model = input('Device Model: ')
vars_dict['gateway_ip'] = input('Managment Gateway Address: ')
mgmt_address = input('Management IP and CIDR: ')
vars_dict['mgmt_ip'] = mgmt_address.split('/')[0]
vars_dict['mgmt_cidr'] = mgmt_address.split('/')[1]

if device_model == 'EX2300-48':
    interface_count = 48
elif device_model == 'EX2300-24':
    interface_count = 24
else:
    interface_count = 12

interface_list = []
iteration = 0
while interface_count > iteration:
    interface_id = str(iteration)
    interface_list.append('ge-0/0/' + interface_id)
    iteration = iteration + 1 

vars_dict['userInterfaces'] = interface_list

# Builds the objects that we will be calling throughout the script
templateLoader = jinja2.FileSystemLoader(searchpath="../templates/")
templateEnv = jinja2.Environment(loader=templateLoader)

# Start building the yaml file to fill out the EX-TEMPLATE.conf jinja2 template
vars_template = templateEnv.get_template('switchBuilderVars.yml')
vars_yaml = vars_template.render(vars_dict)
with open(vars_dict['device_name'] + '.yml', 'w') as f:
    print(vars_yaml, file=f)

# Start building the configuration for the device
switch_vars = vars_dict['device_name'] + '.yml'
config_vars = yaml.load(open(switch_vars).read(), Loader=yaml.FullLoader)
conf_template = templateEnv.get_template('EX-TEMPLATE.conf')
config = conf_template.render(config_vars)
config_path = vars_dict['device_name'] + '.conf'
with open(config_path, 'w') as f:
    print(config, file=f)
