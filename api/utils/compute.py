def convert_ram_to_str(ram: int) -> str:
    if ram < 1024:
        return f"{ram} MB"
    return f"{ram // 1024} GB"
