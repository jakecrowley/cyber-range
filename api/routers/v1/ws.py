import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from api.routers.v1.auth import authenticate
from api.models.users import LdapUserInfo
import api.utils.redis as Redis
import asyncio

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, project_id: str, websocket: WebSocket):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

    def disconnect(self, project_id: str, websocket: WebSocket):
        self.active_connections[project_id].remove(websocket)

    async def send_message(
        self,
        project_id: str,
        message: str | dict,
    ):
        if isinstance(message, dict):
            message = json.dumps(message)

        await Redis.get_redis().publish(
            "websocket",
            json.dumps(
                {
                    "broadcast": False,
                    "project_id": project_id,
                    "message": message,
                }
            ),
        )

    async def _send_message(
        self,
        project_id: str,
        message: str,
    ):
        for ws in self.active_connections[project_id]:
            await ws.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def consume(self):
        sub = Redis.get_pubsub()
        await sub.subscribe("websocket")
        while True:
            await asyncio.sleep(0.01)
            message = await sub.get_message(ignore_subscribe_messages=True)
            if message is not None and isinstance(message, dict):
                msg = json.loads(message.get("data"))
                if msg["broadcast"] == True:
                    await self.broadcast(msg["message"])
                elif msg["project_id"] in self.active_connections:
                    await self._send_message(msg["project_id"], msg["message"])


manager = ConnectionManager()


@router.websocket("/ws")
async def ws(websocket: WebSocket, user_info: LdapUserInfo = Depends(authenticate)):
    await manager.connect(user_info.project_id, websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_info.project_id, websocket)


@router.on_event("startup")
async def subscribe():
    asyncio.create_task(manager.consume())
