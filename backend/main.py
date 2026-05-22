import asyncio
import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

app = FastAPI()

socket_app = socketio.ASGIApp(
    sio,
    app
)

@sio.event
async def connect(sid, environ):
    print("Connected:", sid)


@sio.event
async def user_message(sid, data):

    steps = [

        "🔍 Understanding trip...",

        "✈️ Searching transport...",

        "🏨 Finding hotels...",

        "🎯 Looking for activities...",

        "🧠 Creating itinerary...",

        "✅ Trip ready"
    ]

    for step in steps:

        await sio.emit(
            "ai_status",
            {"message": step},
            room=sid
        )

        await asyncio.sleep(2)