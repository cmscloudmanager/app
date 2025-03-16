import yaml

def build_manifest(project, provider):
    # Define the data as a Python dictionary
    data = {
        'provider': {
            'type': 'hetzner',
            'api_key': provider['apiKey'],
        },
        'instance': 'cpx21',
        'server_name': 'patrick-test',
        'uuid': '2d917d6c-0c69-46c5-bd1d-',  # Example UUID (replace with actual)
        'image': 'debian',
        'lets_encrypt_email': 'void@fuckwit.dev',
        'components': [
            {
                'name': 'wordpress-1',
                'type': 'wordpress',  # Adjust as necessary for Docker
                'config': '...'
            },
            {
                'name': 'mariadb-1',
                'type': 'mariadb',
                'config': '...'
            },
            {
                'name': 'jellyfin',
                'type': 'docker-compose',
                'compose_file': '''
    services:
        bla:
            image: jellyfin
    '''
            }
        ]
    }

    # Convert the dictionary to a YAML string
    yaml_string = yaml.dump(data, default_flow_style=False, sort_keys=False)

    return yaml_string