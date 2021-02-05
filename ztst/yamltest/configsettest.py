import yaml

with open('configset.yml') as f:
    configset = yaml.load(f)

valid_data_keys = configset["data"].keys()
valid_embedding_keys = configset["embeddings"].keys()

print(valid_embedding_keys)
print(valid_data_keys)