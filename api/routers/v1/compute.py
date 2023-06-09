from fastapi import APIRouter, Depends, Cookie

from api.utils.compute import convert_ram_to_str
from api.utils.opnstk import OpenStack
from api.models.users import LdapUserInfo
from .auth import authenticate

router = APIRouter()


@router.post(
    "/compute/create_vm",
    tags=["Compute"],
)
def create_vm(
    user_info: LdapUserInfo = Depends(authenticate),
    vm_name: str = None,
    flavor: str = None,
    image: str = None,
    network: str = None,
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"
    vm = openstack.create_instance(project_name, image, flavor, network, vm_name)
    return {"err": False, "vm-id": vm.id}


@router.get(
    "/compute/list_vms",
    tags=["Compute"],
)
def list_vms(user_info: LdapUserInfo = Depends(authenticate)):
    openstack = OpenStack.Instance()
    servers = openstack.list_instances(user_info.project_id)
    return {
        "err": False,
        "vms": [
            {
                "id": server.id,
                "name": server.name,
                "ip": server.access_ipv4,
                "vcpus": server.flavor.vcpus,
                "memory": convert_ram_to_str(server.flavor.ram),
                "disk": server.flavor.disk,
                "status": server.status,
            }
            for server in servers
        ],
    }