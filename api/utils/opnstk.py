import openstack
from openstack.connection import Connection
from openstack.identity.v3.project import Project
from openstack.network.v2.network import Network
from openstack.compute.v2.server import Server
from openstack.network.v2.subnet import Subnet
from openstack.network.v2.router import Router
from keystoneauth1.session import Session

_instance = None


class OpenStack:
    conn: Connection = None

    def Instance() -> "OpenStack":
        global _instance
        if _instance is None:
            _instance = OpenStack()
        return _instance

    def __init__(self):
        self.conn = openstack.connect(cloud="cyberrange")

    # Project related functions

    def get_project(self, project_name: str) -> Project:
        return self.conn.get_project(project_name)

    def create_project(self, project_name: str) -> Project:
        project: Project = self.conn.create_project(
            name=project_name, domain_id="default"
        )
        self.conn.grant_role(
            name_or_id="admin", user="admin", project=project_name, domain="default"
        )
        return project

    # Networking related functions

    def create_network(self, project_name: str, cidr: str):
        from api.utils.networking import get_dhcp_allocation_pools

        if cidr in self.get_subnets():
            return False

        project: Connection = self.conn.connect_as_project(project_name)
        network: Network = project.create_network(name=project_name)
        subnet: Subnet = project.create_subnet(
            network_name_or_id=network.id,
            cidr=cidr,
            enable_dhcp=True,
            subnet_name=project_name,
            allocation_pools=get_dhcp_allocation_pools(cidr),
            dns_nameservers=["8.8.8.8", "1.1.1.1"],
        )

        main_router: Router = self.conn.get_router("cyber-range-main")
        project.add_router_interface(main_router, subnet_id=subnet.id)
        return True

    def get_subnets(self, project_name: str = None) -> list[str]:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        return [subnet.cidr for subnet in project.list_subnets()]

    # Compute related functions

    def create_instance(
        self,
        project_name: str,
        image_name: str,
        flavor_name: str,
        network_name: str,
        name: str,
    ) -> Server:
        project: Connection = self.conn.connect_as_project(project_name)
        return project.create_server(
            name=name, image=image_name, flavor=flavor_name, network=network_name
        )

    def list_instances(self, project_id: str = None) -> list[Server]:
        servers = self.conn.list_servers(all_projects=True, filters={"project_id": project_id})
        return servers
    
    def start_instance(self, vm_id: str, project_name: str = None):
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)
            
        instance: Server = project.get_server(vm_id)
        instance.start()

    def stop_instance(self, vm_id: str, project_name: str = None):
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)
            
        instance: Server = project.get_server(vm_id)
        instance.stop()
        
        
