import random

used_subnets = ["192.168.0.0/24", "10.176.35.0/24"]

def gen_private_subnet():
    subnet = random.choice(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"])
    [prefix_address, net_size] = subnet.split("/")
    net_size = int(net_size)
    #Convert ip address to 32 bit binary
    octet_list_int = prefix_address.split(".")
    octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
    ip_bin = ("").join(octet_list_bin)
    #Extract Network ID from 32 binary
    network = ip_bin[0:32-(32-net_size)]
    #Add random number in remaining bits
    for i in range(32-net_size):
        network += str(random.randint(0,1))
    #Convert back to decimal
    octet_list_bin = [network[i:i+8] for i in range(0, len(network)-8, 8)]
    octet_list_int = [str(int(i, 2)) for i in octet_list_bin]
    return (".").join(octet_list_int) + ".0/24"

def get_unused_private_subnet():
    subnet = gen_private_subnet()
    if subnet in used_subnets:
        return get_unused_private_subnet()
    return subnet

if __name__ == "__main__":
    print(get_unused_private_subnet())