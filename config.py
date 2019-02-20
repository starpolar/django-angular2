import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, ".env")
load_dotenv(dotenv_path=env_path)


class Config(object):
    cloudant_username = os.environ.get('cloudant_username')
    cloudant_password = os.environ.get('cloudant_password')
    cloudant_apikey = os.environ.get('cloudant_apikey')
    cloudant_databasename = os.environ.get('cloudant_databasename')
    cloudant_url = os.environ.get('cloudant_url')
