import hashlib
import getpass
import os
import argparse
import json
import sys
import pyperclip
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet

def setup():
    """ Set up secrets.json """
    print('Welcome to Alcazar! Enter master password which will be used to encrypt secrets.')
    master_pass = getpass.getpass('Master password:')

    with open('./secrets.json', 'w') as secrets_file:
        salt = b64encode(os.urandom(32))

        secret_key = hashlib.pbkdf2_hmac('sha256', bytes(master_pass, 'utf-8'), salt, 1000000, 32)

        fernet_session = Fernet(b64encode(secret_key))

        # Test secret used to verify that correct password is given
        password_check = b64encode(fernet_session.encrypt(b64encode(os.urandom(32)))).decode('utf-8')

        secrets = {
            'salt': salt.decode('utf-8'),
            'password_check': password_check 
        }

        json.dump(secrets, secrets_file)

def get_secrets():
    """ Load encrypted secrets from secrets.json """
    with open('./secrets.json', 'r') as secrets_file:
        secrets = json.load(secrets_file)

    if not secrets.get('salt'):
        raise KeyError('Could not find salt')
    if not secrets.get('password_check'):
        raise KeyError('Could not find password_check secret. Unable to verify password.')

    return secrets

def start_fernet_session(secrets):
    """ Start a Fernet session """
    user_password = getpass.getpass()

    encrpyted_user_pass = hashlib.pbkdf2_hmac('sha256', bytes(user_password, 'utf-8'), bytes(secrets['salt'], 'utf-8'), 1000000, 32)

    fernet_session = Fernet(b64encode(encrpyted_user_pass))

    # Test that encrpyted_user_pass is the correct secret key
    retrieve_secret(secrets, 'password_check', fernet_session)

    return fernet_session

def retrieve_secret(secrets, secret_name, fernet_session):
    """ Retrieve a secret from a given secret name and fernet session """
    secret_value = secrets[secret_name]

    return fernet_session.decrypt(b64decode(bytes(secret_value, 'utf-8'))).decode("utf-8")

def save_secret(secret_name, secret_value, secrets, fernet_session):
    """ Save a secret with a given secret name and fernet session """
    encrypted_secret = b64encode(fernet_session.encrypt(bytes(secret_value, 'utf-8'))).decode('utf-8')

    with open('./secrets.json', 'w+') as secrets_file:
        secrets[secret_name] = encrypted_secret
        json.dump(secrets, secrets_file)


if __name__ == '__main__':
    if not os.path.isfile('./secrets.json'):
        setup()
        sys.exit(0)

    arg_parser = argparse.ArgumentParser() 
    arg_parser.add_argument('-r', help='Retrieve a secret with a given name')
    arg_parser.add_argument('-s', help='Save a secret with a given name')
    arg_parser.add_argument('-l', help='List the names of all stored secrets', action='store_true')
    args = arg_parser.parse_args()

    # Validate arg length
    if len(sys.argv) == 1:
        print('No actions specified. Exiting.')
        sys.exit(0)

    if len(sys.argv) > 3:
        print('Max arguments exceeded. You many only do one thing at a time.')
        sys.exit(0)

    # Get encrypted secrets
    secrets = get_secrets()

    if args.l:
        for secret_name in secrets:
            if secret_name not in ('salt', 'password_check'):
                print(secret_name)
        
        sys.exit(0)

    # Validate input
    if args.r or args.s:
        if args.r in ('salt', 'password_check'):
            print(f'Cannot use {args.r or args.s} as a secret name')
            sys.exit(0)

        if not secrets.get(args.r or args.s):
            print(f'Could not find secret {args.r or args.s}')
            sys.exit(0)

    fernet_session = start_fernet_session(secrets)

    if args.r:
        secret = retrieve_secret(secrets, args.r, fernet_session)
        
        # Copy secret to clipboard
        pyperclip.copy(secret)
        print(f'Copied {args.r} to clipboard')

        sys.exit(0)

    if args.s:
        if args.s in ('salt', 'password_check'):
            print(f'Cannot use {args.s} as a secret name')
            sys.exit(0)

        print('Enter the secret string you want to store.')
        secret_value = getpass.getpass('Secret: ')

        save_secret(args.s, secret_value, secrets, fernet_session)
        print(f'Successfully stored {args.s}')

        sys.exit(0)

