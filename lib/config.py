# from dataclasses import dataclass

import yaml

# class Config(dataclass):
#     mail =

with open('secure.yml', 'r') as f:
    config = yaml.safe_load(f)
