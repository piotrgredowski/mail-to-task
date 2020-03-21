from dataclasses import dataclass

import yaml
from dacite import from_dict as dataclass_from_dict


@dataclass
class Sender:
    address: str
    password: str
    server_address: str
    server_port: int


@dataclass
class SecureConfig:
    sender: Sender


@dataclass
class Config:
    secure: SecureConfig
    a: int


def parse_yaml(path: str) -> dict:
    with open(path, "r") as f:
        yaml_as_dict = yaml.safe_load(f)

    return yaml_as_dict


secure_raw = parse_yaml("secure.yml")
config_raw = parse_yaml("config.yml")
config_raw.update({"secure": secure_raw})


config: Config = dataclass_from_dict(data_class=Config, data=config_raw)
