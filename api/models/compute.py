from pydantic import BaseModel


class CreateVMInfo(BaseModel):
    vm_name: str
    vcpus: int
    memory: int
    disk: int
    image_id: str
    network_id: str
    keypair_name: str | None


class CreateVMResponse(BaseModel):
    err: bool
    vm_id: str


class CreateKeypairInfo(BaseModel):
    name: str


class CreateKeypairResponse(BaseModel):
    err: bool
    name: str | None
    private_key: str | None
    msg: str | None
