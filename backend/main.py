import socketio
from fastapi import FastAPI

from graph.workflow import graph
from memory.session_store import sessions


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)


@sio.event
async def connect(sid, environ):
    sessions[sid] = {"messages": [], "pending_options": []}
    print(f"Connected: {sid}")
    await sio.emit(
        "ai_status",
        {"message": "Hey 👋 Where are we traveling today?", "options": []},
        room=sid,
    )


@sio.event
async def disconnect(sid):
    sessions.pop(sid, None)
    print(f"Disconnected: {sid}")


@sio.event
async def user_message(sid, data):

    text = data.get("text", "").strip()
    if not text:
        return

    sessions[sid]["messages"].append(f"User: {text}")
    # Clear previous options so they don't persist in state
    sessions[sid]["pending_options"] = []

    try:
        result = graph.invoke(sessions[sid])
        sessions[sid].update(result)

        last_msg = result["messages"][-1]
        display_msg = last_msg.removeprefix("AI: ")

        # ← Read options from the agent result
        options = result.get("pending_options", [])

        if result.get("itinerary") and result.get("itinerary_done"):
            await sio.emit(
                "itinerary_ready",
                {
                    "message": display_msg,
                    "itinerary": result["itinerary"],
                },
                room=sid,
            )
        else:
            await sio.emit(
                "ai_status",
                {
                    "message": display_msg,
                    "options": options,   # ← chips sent here
                },
                room=sid,
            )

    except Exception as e:
        print(f"Graph error: {e}")
        await sio.emit(
            "ai_status",
            {"message": "Something went wrong! Try again.", "options": []},
            room=sid,
        )