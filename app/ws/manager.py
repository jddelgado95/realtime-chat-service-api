import json
import redis.asyncio as aioredis
from fastapi import WebSocket, HTTPException
from typing import Dict, List
from app.core.security import verify_token

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}
        self.redis = aioredis.from_url("redis://redis:6379")

    async def connect(self, channel_id: str, ws: WebSocket, user: str):
        await ws.accept()
        self.active.setdefault(channel_id, []).append(ws)
        await self.redis.publish(f"{channel_id}:presence", json.dumps({"join": user}))

    async def disconnect(self, channel_id, ws, user):
        self.active[channel_id].remove(ws)
        await self.redis.publish(f"{channel_id}:presence", json.dumps({"leave": user}))

    async def broadcast(self, channel_id, user, msg):
        payload = {"user": user, "message": msg["text"]}
        await self.redis.publish(channel_id, json.dumps(payload))
        for conn in self.active[channel_id]:
            await conn.send_json(payload)

    def authenticate(self, token: str) -> str:
        email = verify_token(token)
        if not email:
            raise HTTPException(401, "Invalid token")
        return email

    async def get_token_header(self, websocket: WebSocket):
        token = websocket.query_params.get("token")
        if not token:
            raise HTTPException(401, "Missing token")
        return token