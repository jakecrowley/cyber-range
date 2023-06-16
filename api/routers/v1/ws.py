import json
import api.utils.redis as Redis


class ConnectionManager:
    async def broadcast_message(
        self,
        message: str | dict,
    ):
        if isinstance(message, dict):
            message = json.dumps(message)

        await Redis.get_redis().publish(
            "websocket",
            json.dumps(
                {
                    "broadcast": True,
                    "message": message,
                }
            ),
        )
    
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


manager = ConnectionManager()
