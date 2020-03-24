from dataclasses import dataclass
import typing

from ruamel.yaml import YAML

from dacite import from_dict as dataclass_from_dict

yaml = YAML(typ="safe")


@dataclass
class Sender:
    address: str
    password: str
    server_address: str
    server_port: int


@dataclass
class Receiver:
    address: str


@dataclass
class Trello(Receiver):
    api_key: str
    api_secret: str


@dataclass
class SecureConfig:
    sender: Sender
    trello: Trello


@dataclass
class TaskRequired:
    received_from: str


@dataclass
class TrelloHandlerOptionDueDate:
    month: int
    day_of_month: int
    hour: int
    minute: int


@dataclass
class TrelloHandlerOptions:
    board: str
    list_name: str
    labels: typing.List[str]
    assignee: str
    due_date: TrelloHandlerOptionDueDate


@dataclass
class Handler:
    name: str
    options: typing.Union[TrelloHandlerOptions]


@dataclass
class Task:
    name: str
    required: TaskRequired
    handler: Handler


@dataclass
class Config:
    secure: SecureConfig
    tasks: typing.List[Task]


def parse_yaml(path: str) -> dict:
    with open(path, "r") as f:
        yaml_as_dict = yaml.load(f)

    return yaml_as_dict


secure_raw = parse_yaml("secure.yml")
config_raw = parse_yaml("config.yml")
config_raw.update({"secure": secure_raw})

config: Config = dataclass_from_dict(data_class=Config, data=config_raw)
config.tasks[0].handler.options.assignee
