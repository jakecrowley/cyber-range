from fastapi import APIRouter, Depends

from api.utils.opnstk import OpenStack
from api.models.users import LdapUserInfo
from api.models import CreateNetworkInfo, CreateNetworkResponse
from .auth import authenticate

from pprint import pprint

router = APIRouter()


@router.get(
    "/networking/get_networks",
    tags=["Networking"],
)
def get_networks(
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    # pprint(openstack.get_project_ports(project_name))

    networks = openstack.get_subnets(project_name)

    return {
        "err": False,
        "networks": [
            {
                "id": network.id,
                "name": network.name,
                "cidr": network.cidr,
                "gateway_ip": network.gateway_ip,
                "dns": network.dns_nameservers,
            }
            for network in networks
        ],
    }


@router.get(
    "/networking/get_subnets",
    tags=["Networking"],
)
def get_subnets(
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    subnets = openstack.get_subnets(project_name)

    return {"err": False, "subnets": subnets}


@router.post(
    "/networking/create_network",
    tags=["Networking"],
    response_model=CreateNetworkResponse,
)
def create_network(
    network_info: CreateNetworkInfo,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    result = openstack.create_network(project_name, network_info.cidr, network_info.name)

    if result:
        return CreateNetworkResponse(err=False, msg=None)
    else:
        return CreateNetworkResponse(err=True, msg="Network already exists or invalid CIDR")


@router.get(
    "/networking/delete_network",
    tags=["Networking"],
    response_model=CreateNetworkResponse,
)
def delete_network(
    network_id: str,
    user_info: LdapUserInfo = Depends(authenticate),
):
    openstack = OpenStack.Instance()
    project_name = f"cyberrange-{user_info.username}"

    result = openstack.delete_network(project_name, network_id)

    if result:
        return CreateNetworkResponse(err=False, msg=None)
    else:
        return CreateNetworkResponse(err=True, msg="Failed to delete network")
