import yaml

with open('/home/kamlesh/PycharmProjects/today/lib/config.yaml', 'r') as f:
    doc = yaml.load(f)

def handler(tree,node):
    return doc[tree][node]

