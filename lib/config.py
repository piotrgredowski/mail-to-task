from dataclasses import dataclass
import typing

from ruamel.yaml import YAML
from pydantic import BaseModel


yaml = YAML(typ="safe")


class Sender(BaseModel):
    address: str
    password: str
    server_address: str
    server_port: int


class Receiver(BaseModel):
    address: str


class Trello(Receiver):
    api_key: str
    api_secret: str


class SecureConfig(BaseModel):
    sender: Sender
    trello: Trello


class TaskRequired(BaseModel):
    received_from: str


class TrelloHandlerOptionDueDate(BaseModel):
    month: int
    day_of_month: int
    hour: int
    minute: int


class TrelloHandlerOptions(BaseModel):
    board: str
    list_name: str
    labels: typing.List[str]
    assignee: str
    due_date: TrelloHandlerOptionDueDate


class Handler(BaseModel):
    name: str
    options: typing.Union[TrelloHandlerOptions]


class Task(BaseModel):
    name: str
    required: TaskRequired
    handler: Handler


class Config(BaseModel):
    secure: SecureConfig
    tasks: typing.List[Task]


def parse_yaml(path: str) -> dict:
    with open(path, "r") as f:
        yaml_as_dict = yaml.load(f)

    return yaml_as_dict


secure_raw = parse_yaml("secure.yml")
config_raw = parse_yaml("config.yml")
config_raw.update({"secure": secure_raw})

config = Config(**config_raw)
