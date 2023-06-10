from fastapi import APIRouter, Depends

from api.utils.compute import convert_ram_to_str, get_ip_from_addresses
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
                "ip": get_ip_from_addresses(server.addresses),
                "vcpus": server.flavor.vcpus,
                "memory": convert_ram_to_str(server.flavor.ram),
                "disk": server.flavor.disk,
                "status": server.status,
            }
            for server in servers
        ],
    }


@router.get(
    "/compute/stop_vm",
    tags=["Compute"],
)
def stop_vm(user_info: LdapUserInfo = Depends(authenticate), vm_id: str = None):
    openstack = OpenStack.Instance()
    openstack.stop_instance(vm_id)
    return {"err": False}


@router.get(
    "/compute/get_console_url",
    tags=["Compute"],
)
def get_console_url(
    user_info: LdapUserInfo = Depends(authenticate), server_id: str = None
):
    openstack = OpenStack.Instance()
    return {
        "err": False,
        "url": openstack.get_console_url(server_id, user_info.project_id)["console"][
            "url"
        ],
    }
