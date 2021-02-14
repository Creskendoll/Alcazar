import hashlib
import getpass
import os
import argparse
import json
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet

# TODO: What if user enters 'salt' or 'password_check' as a key?
# TODO: Add tests
# TODO: Allow rehashing and password reset
# TODO: Add backups to prevent data loss
# TODO: Don't ask for password unless user is retrieving or saving (no need to ask on '--help')
# TODO: Allow more than just one secret per key
# TODO: Display a message if secrets.json doesn't exist
# TODO: Convert to class based model?
# TODO: Allow persistent sessions?

def get_secrets_on_startup():
    """ Load secrets from secrets.json or create secrets.json; get Fernet session """
    user_password = getpass.getpass()

    try:
        with open('secrets.json', 'r') as secrets_file:
            secrets = json.load(secrets_file)

        if not secrets.get('salt'):
            raise KeyError('Could not find salt')
        if not secrets.get('password_check'):
            raise KeyError('Could not find password_check secret. Unable to verify password.')

        encrpyted_user_pass = hashlib.pbkdf2_hmac('sha256', bytes(user_password, 'utf-8'), bytes(secrets['salt'], 'utf-8'), 1000000, 32)

        fernet_session = Fernet(b64encode(encrpyted_user_pass))

        # Test that encrpyted_user_pass is the correct secret key
        retrieve_secret(secrets, 'password_check', fernet_session)

    except FileNotFoundError:
        with open('secrets.json', 'w') as secrets_file:
            salt = b64encode(os.urandom(32))

            encrpyted_master_pass = hashlib.pbkdf2_hmac('sha256', bytes(user_password, 'utf-8'), salt, 1000000, 32)

            fernet_session = Fernet(b64encode(encrpyted_master_pass))

            # Test secret used to verify that correct password is given
            password_check = b64encode(fernet_session.encrypt(b64encode(os.urandom(32)))).decode('utf-8')

            secrets = {
                'salt': salt.decode('utf-8'),
                'password_check': password_check 
            }

            json.dump(secrets, secrets_file)

            secret_key = encrpyted_master_pass

    return secrets, fernet_session

def retrieve_secret(secrets, secret_name, fernet_session):
    """ Retrieve a secret from a given secret name and fernet session """
    secret_value = secrets.get(secret_name)
    
    if not secret_value:
        raise KeyError(f'{secret_name} not found')

    return fernet_session.decrypt(b64decode(bytes(secret_value, 'utf-8'))).decode("utf-8")

def save_secret(secret_name, secret_value, secrets, fernet_session):
    """ Save a secret with a given secret name and fernet session """
    encrypted_secret = b64encode(fernet_session.encrypt(bytes(secret_value, 'utf-8'))).decode('utf-8')

    with open('secrets.json', 'w+') as secrets_file:
        secrets[secret_name] = encrypted_secret
        json.dump(secrets, secrets_file)

if __name__ == '__main__':
    secrets, fernet_session = get_secrets_on_startup()

    arg_parser = argparse.ArgumentParser() 
    arg_parser.add_argument('-r', help='Retrieve a secret with a given name')
    arg_parser.add_argument('-s', help='Save a secret with a given name')
    args = arg_parser.parse_args()

    # TODO: Save secrets to clipboard
    if args.r:
        secret = retrieve_secret(secrets, args.r, fernet_session)
        print(secret)
    elif args.s:
        secret_value = getpass.getpass('Secret: ')
        save_secret(args.s, secret_value, secrets, fernet_session)
