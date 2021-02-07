import yaml
import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# try:
#     with open(PROJECT_ROOT + os.sep + 'yamltest' + os.sep + 'collection.yml') as f:
#         configset = yaml.load(f)
#     collections_l = configset.keys()
#     print(collections_l)
#     oj_knkeys = configset["oj_kn"].keys()
#     print(oj_knkeys)
# except Exception as e:
#     print({'error': str(e)})


import bios
configset = bios.read(PROJECT_ROOT + os.sep + 'yamltest' + os.sep + 'collection.yml', file_type='yaml')
print(configset)
collections_l = configset.keys()
print(collections_l)
oj_knkeys = configset["oj_kn"].keys()
