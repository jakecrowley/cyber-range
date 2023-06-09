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
