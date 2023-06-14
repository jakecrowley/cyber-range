from .opnstk import OpenStack


def convert_ram_to_str(ram: int) -> str:
    if ram < 1024:
        return f"{ram} MB"
    return f"{ram // 1024} GB"


def get_ip_from_addresses(addresses: dict) -> str:
    for network in addresses:
        for ip in addresses[network]:
            if ip["OS-EXT-IPS:type"] == "fixed":
                return ip["addr"]
    return None


def get_or_create_flavor(
    openstack: OpenStack, flavor_name: str, vcpus: int, ram: int, disk: int
):
    flavors = openstack.get_flavors()
    for flavor in flavors:
        if flavor.vcpus == vcpus and flavor.ram == ram and flavor.disk == disk:
            return flavor

    return openstack.create_flavor(vcpus, ram, disk, flavor_name)
