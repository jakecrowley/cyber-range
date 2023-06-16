from fastapi import APIRouter, Depends

from api.utils.opnstk import OpenStack
from api.models.users import LdapUserInfo
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
