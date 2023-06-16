from fastapi import APIRouter, Depends, BackgroundTasks
from threading import Thread

from api.utils.compute import (
    convert_ram_to_str,
    get_ip_from_addresses,
    get_or_create_flavor,
)
from api.utils.opnstk import OpenStack
from api.models.users import LdapUserInfo
from api.models.compute import CreateVMInfo, CreateVMResponse
from api.models import DefaultResponse
from .auth import authenticate
from api.routers.v1.ws import manager
from json import loads

router = APIRouter()


async def send_ws_update(project_id: str, type: str, data: dict):
    await manager.send_message(
        project_id,
        {
            "type": type,
            "data": data,
        },
    )


async def poll_vm_status(old_status: str, vm_id: str, project_id: str):
    openstack = OpenStack.Instance()
    while True:
        server, status = openstack.get_instance_status(vm_id, project_id=project_id)

        if status != old_status and status != "REBOOT":
            if status == "DELETED":
                vm_info = {"id": vm_id, "status": "DELETED"}
            else:
                vm_info = {
                    "id": server.id,
                    "name": server.name,
                    "ip": get_ip_from_addresses(server.addresses),
                    "vcpus": server.flavor.vcpus,
                    "memory": convert_ram_to_str(server.flavor.ram),
                    "disk": server.flavor.disk,
                    "status": server.status,
                }
            await manager.send_message(
                project_id,
                {
                    "type": "INSTANCE_UPDATE",
                    "data": {"vm_id": vm_id, "vm": vm_info},
                },
            )
            return


@router.post(
    "/compute/create_vm",
    tags=["Compute"],
    response_model=CreateVMResponse,
)
def create_vm(
    vm_info: CreateVMInfo,
    background_tasks: BackgroundTasks,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    flavor_name = (
        f"{vm_info.vcpus}vcpu-{convert_ram_to_str(vm_info.memory)}-{vm_info.disk}gb"
    )
    flavor = get_or_create_flavor(
        openstack, flavor_name, vm_info.vcpus, vm_info.memory, vm_info.disk
    )

    vm = openstack.create_instance(
        project_name, vm_info.image_id, flavor.id, vm_info.network_id, vm_info.vm_name
    )

    background_tasks.add_task(
        send_ws_update, user_info.project_id, "INSTANCE_CREATE", {}
    )
    background_tasks.add_task(poll_vm_status, "BUILD", vm.id, user_info.project_id)

    return CreateVMResponse(err=False, vm_id=vm.id)


@router.get("/compute/delete_vm", tags=["Compute"], response_model=DefaultResponse)
async def delete_vm(
    background_tasks: BackgroundTasks,
    vm_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    await send_ws_update(
        user_info.project_id,
        "INSTANCE_STATUS",
        {"vm_id": vm_id, "status": "DELETING"},
    )

    background_tasks.add_task(poll_vm_status, "ACTIVE", vm_id, user_info.project_id)

    res = openstack.delete_instance(project_name, vm_id)

    if res:
        return DefaultResponse(err=False, msg=None)
    return DefaultResponse(err=True, msg=f"Failed to delete VM with id: {vm_id}")


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
                "recommended_specs": loads(image.properties["rec_specs"])
                if "rec_specs" in image.properties
                else None,
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
    await manager.send_message(
        user_info.project_id,
        {
            "type": "INSTANCE_STATUS",
            "data": {"vm_id": vm_id, "status": "STARTING"},
        },
    )

    openstack = OpenStack.Instance()
    openstack.start_instance(vm_id, user_info.project_id)

    background_tasks.add_task(poll_vm_status, "SHUTOFF", vm_id, user_info.project_id)

    return DefaultResponse(err=False, msg=None)


@router.get(
    "/compute/stop_vm",
    tags=["Compute"],
)
async def stop_vm(
    background_tasks: BackgroundTasks,
    vm_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    await manager.send_message(
        user_info.project_id,
        {
            "type": "INSTANCE_STATUS",
            "data": {"vm_id": vm_id, "status": "STOPPING"},
        },
    )

    openstack = OpenStack.Instance()
    openstack.stop_instance(vm_id, user_info.project_id)

    background_tasks.add_task(poll_vm_status, "ACTIVE", vm_id, user_info.project_id)
    return DefaultResponse(err=False, msg=None)


@router.get("/compute/reboot_vm", tags=["Compute"])
async def reboot_vm(
    background_tasks: BackgroundTasks,
    vm_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    await manager.send_message(
        user_info.project_id,
        {
            "type": "INSTANCE_STATUS",
            "data": {"vm_id": vm_id, "status": "REBOOT"},
        },
    )

    openstack = OpenStack.Instance()
    openstack.reboot_instance(vm_id, user_info.project_id)

    background_tasks.add_task(poll_vm_status, "SHUTOFF", vm_id, user_info.project_id)
    return DefaultResponse(err=False, msg=None)


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
