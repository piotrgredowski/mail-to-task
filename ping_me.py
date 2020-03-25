import os
from time import sleep

import requests


def ping_me():
    sleep(60)
    print("ping")
    requests.get(os.environ.get("APP_ADDRESS"))


is_debug = os.environ.get("ENVIRONMENT") == "dev"

if not is_debug:
    while True:
        ping_me()
