import socketio
from fastapi import FastAPI

from graph.workflow import graph
from memory.session_store import sessions


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

    sessions[sid] = {
        "messages": []
    }

    print(f"Connected: {sid}")


@sio.event
async def disconnect(sid):

    sessions.pop(sid, None)

    print(f"Disconnected: {sid}")


@sio.event
async def user_message(sid, data):

    text = data["text"]

    sessions[sid]["messages"].append(
        text
    )

    result = graph.invoke(
        sessions[sid]
    )

    sessions[sid].update(
        result
    )

    ai_reply = result["messages"][-1]

    await sio.emit(
        "ai_status",
        {
            "message": ai_reply
        },
        room=sid
    )