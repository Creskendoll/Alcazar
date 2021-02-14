import pytest
import sys
import alcazar
import os
import json
import hashlib
from base64 import b64encode

if os.path.isfile('./secrets.json'):
    print('Cannot run tests because testing process would overwrite ./secrets.json. Move ./secrets.json to another directory.')
    sys.exit(0)


def test__setup():
    master_pass = 'M@$T3r P&$$W0rD_(*SDFU_+'
    alcazar.setup(master_pass)

    with open('./secrets.json', 'r') as secrets_file:
        secrets = json.load(secrets_file)

    assert 'salt' in secrets
    assert len(secrets['salt']) == 44

    assert 'password_check' in secrets
    secret_key = hashlib.pbkdf2_hmac('sha256', bytes(master_pass, 'utf-8'), bytes(secrets['salt'], 'utf-8'), 1000000, 32)
    assert b64encode(secret_key).decode('utf-8') not in json.dumps(secrets)
    assert master_pass not in json.dumps(secrets)

    os.remove('./secrets.json')

def test__get_secrets():
    master_pass = 'M@$T3er P&$$W0rD_(*SDFU_-'
    alcazar.setup(master_pass)

    secrets = alcazar.get_secrets()

    assert 'salt' in secrets
    assert 'password_check' in secrets

    os.remove('./secrets.json')

def test__start_fernet_session():
    master_pass = 'm]@$T3er P&$$W0rD_(*SDFU_---'
    alcazar.setup(master_pass)

    secrets = alcazar.get_secrets()

    fernet_session = alcazar.start_fernet_session(master_pass, secrets)

    os.remove('./secrets.json')

def test__save_secret():
    master_pass = 'm\\]@$T3er P&$$W0rD_(*SDFU_--7-'
    alcazar.setup(master_pass)

    secrets = alcazar.get_secrets()

    fernet_session = alcazar.start_fernet_session(master_pass, secrets)

    alcazar.save_secret('foo', 'bar', secrets, fernet_session)

    assert 'foo' in secrets
    assert 'bar' not in json.dumps(secrets)

    with open('./secrets.json', 'r') as secrets_file:
        file_secrets = json.load(secrets_file)

    assert 'foo' in file_secrets
    assert 'bar' not in json.dumps(file_secrets)

    os.remove('./secrets.json')

def test__retrieve_secret():
    master_pass = 'm\\]@$T3er P&$$W0rD_(*SDFU_--0-'
    alcazar.setup(master_pass)

    secrets = alcazar.get_secrets()

    fernet_session = alcazar.start_fernet_session(master_pass, secrets)

    alcazar.save_secret('foo2', 'bar2', secrets, fernet_session)

    secrets = alcazar.get_secrets()

    bar = alcazar.retrieve_secret('foo2', secrets, fernet_session)

    assert bar == 'bar2'

    with open('./secrets.json', 'r') as secrets_file:
        file_secrets = json.load(secrets_file)

    assert 'foo2' in file_secrets

    file_bar = alcazar.retrieve_secret('foo2', file_secrets, fernet_session)

    assert file_bar == 'bar2'

    os.remove('./secrets.json')

