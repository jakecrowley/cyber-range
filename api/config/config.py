import os
from dotenv import load_dotenv

load_dotenv()

OPENSTACK_PASSWORD = os.getenv('OPENSTACK_PASSWORD')

