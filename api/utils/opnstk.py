import openstack
from openstack.connection import Connection
from keystoneauth1.session import Session


class OpenStack:
    conn: Connection = None

    def __init__(self):
        self.conn = openstack.connect(cloud="cyberrange")

    def create_project(self, project_name: str):
        self.conn.create_project(name=project_name, domain_id="default")
        self.conn.grant_role(
            name_or_id="admin", user="admin", project=project_name, domain="default"
        )


OpenStackAPI: OpenStack = None
