import os
from time import sleep

import requests


def ping_me(address):
    sleep(60)
    print("ping")
    from datetime import datetime

    print(datetime.utcnow())

    # requests.get(address)


# is_debug = os.environ.get("ENVIRONMENT") == "dev"

# if not is_debug:
#     while True:
#         ping_me()
