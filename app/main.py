from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from app.api import auth as auth_router, users as users_router, channels as channels_router
from app.ws.manager import ConnectionManager
from app.config import settings

app = FastAPI(title="Chat Service API")
manager = ConnectionManager()

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(channels_router.router, prefix="/channels", tags=["channels"])

@app.websocket("/ws/{channel_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id: str, token: str = Depends(manager.get_token_header)):
    user = manager.authenticate(token)
    await manager.connect(channel_id, websocket, user)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(channel_id, user, data)
    except WebSocketDisconnect:
        await manager.disconnect(channel_id, websocket, user)