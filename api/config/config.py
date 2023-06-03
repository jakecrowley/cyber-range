import os
from dotenv import load_dotenv

load_dotenv()

OPENSTACK_PASSWORD = os.getenv('OPENSTACK_PASSWORD')
MONGO_CONN_STR = os.getenv('MONGO_CONN_STR')
