from fastapi import APIRouter, Depends, BackgroundTasks

from api.utils.compute import (
    convert_ram_to_str,
    get_ip_from_addresses,
    get_or_create_flavor,
)
from api.utils.opnstk import OpenStack
from api.models.users import LdapUserInfo
from .auth import authenticate
from api.routers.v1.ws import manager

router = APIRouter()


async def poll_vm_status(old_status: str, vm_id: str, project_id: str):
    openstack = OpenStack.Instance()
    while True:
        status = openstack.get_instance_status(vm_id, project_id=project_id)

        if status != old_status and status != "REBOOT":
            await manager.send_message(
                project_id,
                {
                    "type": "INSTANCE_STATUS",
                    "data": {"vm_id": vm_id, "status": status},
                },
            )
            return


@router.post(
    "/compute/create_vm",
    tags=["Compute"],
)
def create_vm(
    vm_name: str,
    vcpus: int,
    memory: int,
    disk: int,
    image_id: str,
    network_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    flavor_name = f"{vcpus}vcpu-{convert_ram_to_str(memory)}-{disk}gb"
    flavor = get_or_create_flavor(openstack, flavor_name, vcpus, memory, disk)

    vm = openstack.create_instance(
        project_name, image_id, flavor.id, network_id, vm_name
    )
    return {"err": False, "vm-id": vm.id}


@router.post(
    "/compute/delete_vm",
    tags=["Compute"],
)
def delete_vm(vm_id: str, user_info: LdapUserInfo = Depends(authenticate)):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    res = openstack.delete_instance(project_name, vm_id)
    if res:
        return {"err": False}
    return {"err": True, "msg": f"Failed to delete VM with id: {vm_id}"}


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
    "/compute/list_images",
    tags=["Compute"],
)
def list_images(user_info: LdapUserInfo = Depends(authenticate)):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"
    images = openstack.get_images(project_name)
    return {
        "err": False,
        "images": [
            {
                "id": image.id,
                "name": image.name,
                "status": image.status,
            }
            for image in images
        ],
    }


@router.get(
    "/compute/start_vm",
    tags=["Compute"],
)
async def start_vm(
    background_tasks: BackgroundTasks,
    vm_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    openstack.start_instance(vm_id, user_info.project_id)

    await manager.send_message(
        user_info.project_id,
        {
            "type": "INSTANCE_STATUS",
            "data": {"vm_id": vm_id, "status": "STARTING"},
        },
    )

    background_tasks.add_task(poll_vm_status, "SHUTOFF", vm_id, user_info.project_id)
    return {"err": False}


@router.get(
    "/compute/stop_vm",
    tags=["Compute"],
)
async def stop_vm(
    background_tasks: BackgroundTasks,
    vm_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    openstack.stop_instance(vm_id, user_info.project_id)

    await manager.send_message(
        user_info.project_id,
        {
            "type": "INSTANCE_STATUS",
            "data": {"vm_id": vm_id, "status": "STOPPING"},
        },
    )

    background_tasks.add_task(poll_vm_status, "ACTIVE", vm_id, user_info.project_id)
    return {"err": False}


@router.get("/compute/reboot_vm", tags=["Compute"])
async def reboot_vm(
    background_tasks: BackgroundTasks,
    vm_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    openstack.reboot_instance(vm_id, user_info.project_id)

    await manager.send_message(
        user_info.project_id,
        {
            "type": "INSTANCE_STATUS",
            "data": {"vm_id": vm_id, "status": "REBOOT"},
        },
    )

    background_tasks.add_task(poll_vm_status, "SHUTOFF", vm_id, user_info.project_id)
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
