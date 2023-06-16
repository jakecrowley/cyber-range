from pydantic import BaseModel


class CreateVMInfo(BaseModel):
    vm_name: str
    vcpus: int
    memory: int
    disk: int
    image_id: str
    network_id: str


class CreateVMResponse(BaseModel):
    err: bool
    vm_id: str
