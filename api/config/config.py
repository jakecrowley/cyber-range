import os
from dotenv import load_dotenv

load_dotenv()

OPENSTACK_PASSWORD = os.getenv("OPENSTACK_PASSWORD")
MONGO_CONN_STR = os.getenv("MONGO_CONN_STR")
LDAP_URI = os.getenv("LDAP_URI")
LDAP_USERNAME = os.getenv("LDAP_USERNAME")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")
LDAP_DOMAIN = os.getenv("LDAP_DOMAIN")
LDAP_DN = os.getenv("LDAP_DN")
