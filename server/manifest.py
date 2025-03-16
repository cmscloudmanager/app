import yaml

def build_manifest(project, provider):
    # Define the data as a Python dictionary
    data = {
        'provider': {
            'type': provider['type'].lower(),
            'api_key': provider['apiKey'],
        },
        'dns': {
            'type': provider['type'].lower(),
            'api_key': provider['apiKey'],
        },
        'instance': project['instance'],
        'server_name': project['name'].replace(' ', '-').lower(),
        'uuid': '2d917d6c-0c69-46c5-bd1d-',
        'image': 'debian',
        'lets_encrypt_email': 'void@fuckwit.dev',
        'components': [
            {
                'name': 'app',
                'type': project['type'].lower(),
                'config': {
                    'hostname': project['url'],
                }
            },
            {
                'name': 'helloworld',
                'type': 'example',
                'config': {
                    'hostname': project['url'],
                }
            },
            {
                'name': 'mariadb',
                'type': 'mariadb',
            }
        ]
    }

    # Convert the dictionary to a YAML string
    yaml_string = yaml.dump(data, default_flow_style=False, sort_keys=False)

    return yaml_string