import json
from fastapi import APIRouter, Depends, BackgroundTasks

from api.utils.compute import convert_ram_to_str, get_ip_from_addresses
from api.utils.opnstk import OpenStack
from api.models.users import LdapUserInfo
from .auth import authenticate
from api.routers.v1.ws import manager

router = APIRouter()


async def poll_vm_status(old_status: str, vm_id: str, project_id: str):
    openstack = OpenStack.Instance()
    while True:
        status = openstack.get_instance_status(vm_id, project_id=project_id)
        print(status)

        if status != old_status:
            await manager.send_message(
                project_id,
                json.dumps(
                    {
                        "type": "INSTANCE_STATUS",
                        "data": {"vm_id": vm_id, "status": status},
                    }
                ),
            )
            return


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
    "/compute/start_vm",
    tags=["Compute"],
)
def start_vm(
    background_tasks: BackgroundTasks,
    user_info: LdapUserInfo = Depends(authenticate),
    vm_id: str = None,
):
    openstack = OpenStack.Instance()
    openstack.start_instance(vm_id, user_info.project_id)
    background_tasks.add_task(poll_vm_status, "SHUTOFF", vm_id, user_info.project_id)
    return {"err": False}


@router.get(
    "/compute/stop_vm",
    tags=["Compute"],
)
def stop_vm(
    background_tasks: BackgroundTasks,
    user_info: LdapUserInfo = Depends(authenticate),
    vm_id: str = None,
):
    openstack = OpenStack.Instance()
    openstack.stop_instance(vm_id, user_info.project_id)
    background_tasks.add_task(poll_vm_status, "ACTIVE", vm_id, user_info.project_id)
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
