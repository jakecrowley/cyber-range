from fastapi import APIRouter

router = APIRouter()

@router.post(
    "/auth/login",
    tags=["Authenticaton"],
)
async def login():
    # do login stuff
    pass

@router.get(
    "/auth/logout",
    tags=["Authentication"],
)
async def logout():
    # do logout stuff
    pass