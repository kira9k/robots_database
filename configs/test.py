import yaml

with open('columns_mapping.yaml', 'r', encoding='utf-8') as f:
    dict_s = yaml.safe_load(f)

print(dict_s)