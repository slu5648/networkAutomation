import jinja2


# Build and a basic configuration that allows NETCONF
device_name = input('Serial Number of Device: ')
templateLoader = jinja2.FileSystemLoader(searchpath="../templates/")
templateEnv = jinja2.Environment(loader=templateLoader)
conf_template = templateEnv.get_template('junosBasic.conf')
config = conf_template.render(deviceName=device_name)

with open(device_name + '.conf', 'w') as f:
    print(config, file=f)
