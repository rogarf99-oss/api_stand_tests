
import configuration
import requests

def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH, json=body)

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

