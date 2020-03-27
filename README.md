# mail-to-task

Use Python 3.8.2.

Create `.env` file containing:
```
export ENVIRONMENT=dev
export CONFIGS_KEY=abcd # string used for encrypting and decrypting configuration files
export TRELLO_TOKEN=efgh # token for trello
```

Prepare env:
```
python -m venv .venv
source ./prepare_env.sh
```

Install requirements

```
pip install -r requirements.txt
# Requirements for development
pip install -r requirements-dev.txt
```

## Encrypting & decrypting configs

Configs can be stored in encrypted files. Reason? I want to deploy app to Heroku and don't want to store sensitive data in environmental variables there.
```bash
python -m lib.crypting decrypt
python -m lib.crypting encrypt
```

## Running

When developing run with
```
python -m mail_to_task.__init__
```