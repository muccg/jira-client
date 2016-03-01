import sys
import time
import ConfigParser
import os.path
import getpass
import requests
from requests.auth import HTTPBasicAuth

import config

def _get_credentails(config_file_path):
    
    config_parser = ConfigParser.RawConfigParser()
    if os.path.exists(config_file_path):
        config_parser.read(config_file_path)
        username = config_parser.get(config._SECTION, "username")
        password = config_parser.get(config._SECTION, "password")
    else:
        print("Your JIRA creadentials will be saved in %s" % (_get_config_file()))
        username = input("Username: ")
        password = getpass.getpass("Password: ")
    
        config_parser.add_section(config._SECTION)
        config_parser.set(config._SECTION, "username", username)
        config_parser.set(config._SECTION, "password", password)
    
        with open(config_file_path, "wb") as config_file:
            config_parser.write(config_file)

    return username, password

def _get_home_directory():
    return os.path.expanduser("~")

def _get_config_file():
    return os.path.join(_get_home_directory(), config._CONFIG_FILE)

def print_progress(index, total):
    sys.stdout.write("\rTicket %d out of %d done" % (index, total))
    sys.stdout.flush()

def validate_credentials():
    username, password = _get_credentails(_get_config_file())
    params = {"username": username}
    results = requests.get(config._BASE_URL + config._USER, auth=HTTPBasicAuth(username, password), params=params)
    if results.status_code == 401:
        return False
    return True

def get_request_auth(api_call, params=None, json=True):
    username, password = _get_credentails(_get_config_file())
    if params:
        results = requests.get(config._BASE_URL + api_call, auth=HTTPBasicAuth(username, password), params=params)
    else:
        results = requests.get(config._BASE_URL + api_call, auth=HTTPBasicAuth(username, password))
    if results:
        if json:
            return results.json()
        return results
    else:
        None

def put_request_auth(api_call, payload):
    username, password = _get_credentails(_get_config_file())
    headers = {"Content-Type": "application/json; charset=utf8"}
    result = requests.put(config._BASE_URL + api_call, auth=HTTPBasicAuth(username, password), headers=headers, json=payload)
    if result.status_code == 204:
        return True
    return False

def add_label_payload(label):
    return {
        "update":
            {"labels":
                [
                    {"add":"%s" % label}
                ]
            }
        }
