from aiohttp import web
import socketio
import asyncio
import json
import jwt_util
from redis_util import Redis


sio = socketio.AsyncServer(
    cors_allowed_origins=["https://cyberrange.jakecrowley.com"],
)

redis = Redis()
app = web.Application()
sio.attach(app)

clients = {}


@sio.event
def connect(sid, environ):
    if environ["HTTP_TOKEN"]:
        token = environ["HTTP_TOKEN"]
        payload = jwt_util.decode_token(token)
        if payload["project_id"] not in clients:
            clients[payload["project_id"]] = []

        clients[payload["project_id"]].append(sid)
        print("connect ", payload["project_id"], sid)
    else:
        return False


@sio.event
async def chat_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    for client in clients:
        if sid in clients[client]:
            clients[client].remove(sid)
    print("disconnect ", sid)


async def consume():
    sub = redis.get_pubsub()
    await sub.subscribe("websocket")
    while True:
        await asyncio.sleep(0.01)
        message = await sub.get_message(ignore_subscribe_messages=True)
        if message is not None and isinstance(message, dict):
            msg = json.loads(message.get("data"))
            if msg["broadcast"] == True:
                await sio.emit(msg["type"], json.loads(msg["message"]))
            elif msg["project_id"] in clients:
                message = json.loads(msg["message"])
                for client in clients[msg["project_id"]]:
                    await sio.emit(message["type"], message["data"], to=client)


async def on_startup(app):
    asyncio.create_task(consume())


if __name__ == "__main__":
    app.on_startup.append(on_startup)
    web.run_app(app, host="127.0.0.1", port=8001)
