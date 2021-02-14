# Alcazar
Simple & secure password-based secret management using the cryptography library & pbkdf2. Stores secrets by name in a json file using symmetric key encryption. Pbkdf2 is used to generate the secret key.

## Setup
1. Clone Alcazar
2. Install required packages `pip install -r requirements.txt`
3. Set up master password `python alcazar.py`

## Run tests
1. If you have a `./secrets.json` file, move it to another directory because the testing process would overwrite it.
2. Run `pytest`

## Usage
```
usage: alcazar.py [-h] [-r R] [-s S] [-l]

optional arguments:
  -h, --help  show this help message and exit
  -r R        Retrieve a secret with a given name and copy to clipboard
  -s S        Save a secret with a given name
  -l          List the names of all stored secrets
```

