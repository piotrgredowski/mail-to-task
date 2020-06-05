#!/usr/bin/env python3

import os
import sys

from cryptography.fernet import Fernet

key = os.environ.get("CONFIGS_KEY")

if key is not None:
    fernet = Fernet(key)
else:
    print("Environmental variable CONFIGS_KEY is empty")

CONFIG_NAMES = ["secure", "config"]

# TODO: dry it...


def encrypt():
    for name in CONFIG_NAMES:
        not_secure_path = f"{name}.yml"
        secure_path = f"encrypted.{name}"
        if not os.path.exists(not_secure_path):
            raise Exception(f"{not_secure_path} not exists")
        with open(not_secure_path, "rb") as not_secure:
            overwrite = True
            if os.path.exists(secure_path):
                overwrite = input(f"Overwrite {secure_path}?").lower() in ["y", "yes"]
            if overwrite:
                with open(secure_path, "wb") as secure:
                    encrypted = fernet.encrypt(not_secure.read())
                    secure.write(encrypted)
                    print(f"{not_secure_path} encrypted\n")


def decrypt():
    for name in CONFIG_NAMES:
        not_secure_path = f"{name}.yml"
        secure_path = f"encrypted.{name}"
        if not os.path.exists(secure_path):
            raise Exception(f"{secure_path}. not exists")
        with open(secure_path, "rb") as secure:
            overwrite = True
            if os.path.exists(not_secure_path):
                overwrite = input(f"Overwrite {not_secure_path}?").lower() in [
                    "y",
                    "yes",
                ]
            if overwrite:
                with open(not_secure_path, "wb") as not_secure:
                    decrypted = fernet.decrypt(secure.read())
                    not_secure.write(decrypted)
                    print(f"{secure_path} decrypted\n")


if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == "encrypt":
        encrypt()
    elif mode == "decrypt":
        decrypt()
    else:
        print("Need to pass mode: encrypt/decrypt")
