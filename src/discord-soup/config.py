import yaml

def read_auth_key():
    file = open('auth.key')
    auth_key = file.readline()
    file.close()
    return auth_key

def read_config():
    with open('config.yaml') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None