import docker
from string import Template


def load_template(path):
    with open(path, 'r') as f:
        return Template(f.read())

def main():
    client = docker.from_env()
    containers = client.containers.list()

    default_template = load_template('default.template')
    for container in containers:
        env = container.attrs['Config']['Env']
        env = dict([value.split('=') for value in env if 'VIRTUAL' in value])
        env = {k.replace('VIRTUAL_', ''):v for k,v in env.items()}
        if not env:
            continue
        if 'TEMPLATE' in env:
            template = load_template(env['TEMPLATE'] + '.template')
        else:
            template = default_template
        if 'DEST' not in env:
            env['DEST'] = '/'
        print(template.substitute(env))


if __name__ == "__main__":
    main()
