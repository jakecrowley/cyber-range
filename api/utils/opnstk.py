import openstack
from openstack.connection import Connection
from openstack.identity.v3.project import Project
from openstack.network.v2.network import Network
from openstack.network.v2.port import Port
from openstack.compute.v2.flavor import Flavor
from openstack.compute.v2.server import Server
from openstack.compute.v2.image import Image
from openstack.network.v2.subnet import Subnet
from openstack.network.v2.router import Router
from keystoneauth1.session import Session
from novaclient.v2.client import Client
import novaclient.client as nova

_instance = None


class OpenStack:
    conn: Connection = None
    nova: Client = None

    def Instance() -> "OpenStack":
        global _instance
        if _instance is None:
            _instance = OpenStack()
        return _instance

    def __init__(self):
        self.conn = openstack.connect(cloud="cyberrange")
        self.nova = nova.Client(2, session=self.conn.session)

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

        if cidr in self.get_subnets_cidr():
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

    def get_subnets_cidr(self, project_name: str = None) -> list[str]:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        return [subnet.cidr for subnet in project.list_subnets()]

    def get_subnets(self, project_name: str = None) -> list[Subnet]:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        project_id = project.current_project_id
        subnets: list[Subnet] = project.list_subnets()

        return [subnet for subnet in subnets if subnet.project_id == project_id]

    def get_networks(self, project_name: str = None) -> list[Network]:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        return project.list_networks()

    def get_project_ports(self, project_name: str = None) -> list[Port]:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        return [
            port
            for port in project.list_ports()
            if port.location.project.name == project_name
        ]

    # Compute related functions

    def create_instance(
        self,
        project_name: str,
        image_name: str,
        flavor_name: str,
        network_name: str,
        keypair_name: str | None,
        name: str,
    ) -> Server:
        project: Connection = self.conn.connect_as_project(project_name)
        return project.create_server(
            name=name,
            image=image_name,
            flavor=flavor_name,
            network=project_name,
            ip_pool=network_name,
            terminate_volume=True,
            key_name=keypair_name,
        )

    def delete_instance(self, project_name: str, instance_id: str) -> bool:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        return project.delete_server(instance_id, delete_ips=True)

    def list_instances(self, project_id: str = None) -> list[Server]:
        servers = self.conn.list_servers(
            all_projects=True, filters={"project_id": project_id}
        )
        return servers

    def get_flavors(self) -> list[Flavor]:
        return self.conn.list_flavors()
    
    def get_keypairs(self, project_name: str = None) -> list:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        return project.list_keypairs()
    
    def create_flavor(self, vcpus: int, ram: int, disk: int, name: str) -> Flavor:
        flavor: Flavor = self.conn.create_flavor(
            name=name, ram=ram, vcpus=vcpus, disk=disk
        )
        self.conn.set_flavor_specs(
            flavor,
            {
                "hw:cpu_max_cores": f"{vcpus}",
                "hw:cpu_max_sockets": "1",
                "hw:cpu_max_threads": "1",
            },
        )
        return flavor

    def get_images(self, project_name: str = None) -> list[Image]:
        project = self.conn
        if project_name:
            project = self.conn.connect_as_project(project_name)

        images: list[Image] = project.list_images()

        return [image for image in images if image.visibility == "public"]

    def get_instance_status(self, server_id: str, project_id: str = None) -> str:
        instance: Server = self.conn.get_server(server_id, all_projects=True)

        if instance is None:
            return (None, "DELETED")

        if instance.project_id != project_id:
            raise Exception("Unauthorized")

        return (instance, instance.status)

    def get_console_url(self, server_id: str, project_name: str) -> str:
        instance: Server = self.conn.get_server(server_id, all_projects=True)

        if instance.project_id != project_name:
            raise Exception("Unauthorized")

        return self.nova.servers.get_vnc_console(instance, "novnc")

    def start_instance(self, vm_id: str, project_id: str = None):
        instance: Server = self.conn.get_server(vm_id, all_projects=True)
        if instance.project_id != project_id:
            raise Exception("Unauthorized")

        self.nova.servers.start(instance)

    def stop_instance(self, vm_id: str, project_id: str = None):
        instance: Server = self.conn.get_server(vm_id, all_projects=True)
        if instance.project_id != project_id:
            raise Exception("Unauthorized")

        self.nova.servers.stop(instance)

    def reboot_instance(
        self, vm_id: str, project_id: str = None, reboot_type: str = "SOFT"
    ):
        instance: Server = self.conn.get_server(vm_id, all_projects=True)
        if instance.project_id != project_id:
            raise Exception("Unauthorized")

        self.nova.servers.reboot(instance, reboot_type)
