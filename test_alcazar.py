import pytest
import sys
import alcazar
import os

if os.path.isfile('./secrets.json'):
    print('Cannot run tests because testing process would overwrite ./secrets.json. Move ./secrets.json to another directory.')
    sys.exit(0)

def test_setup():
    pass

def test_get_secrets():
    pass

def test_start_fernet_session():
    pass

def test_retrieve_secret():
    pass

def test_save_secret():
    pass

