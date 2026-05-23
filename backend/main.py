import socketio
from fastapi import FastAPI

from graph.workflow import graph
from memory.session_store import sessions


sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)

app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)


@sio.event
async def connect(sid, environ):
    sessions[sid] = {"messages": []}
    print(f"Connected: {sid}")
    # ← Send welcome message from server instead of hardcoding it in the frontend
    await sio.emit("ai_status", {"message": "Hey 👋 Where are we traveling today?"}, room=sid)


@sio.event
async def disconnect(sid):
    sessions.pop(sid, None)
    print(f"Disconnected: {sid}")


@sio.event
async def user_message(sid, data):

    text = data.get("text", "").strip()
    if not text:
        return

    # ← Store with speaker label so the LLM knows who said what
    sessions[sid]["messages"].append(f"User: {text}")

    try:
        result = graph.invoke(sessions[sid])
        sessions[sid].update(result)

        last_msg = result["messages"][-1]
        display_msg = last_msg.removeprefix("AI: ")  # strip prefix before sending to frontend

        # ← If itinerary was just generated, emit a richer event with the JSON
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
                {"message": display_msg},
                room=sid,
            )

    except Exception as e:
        # ← Catch errors so the frontend doesn't hang forever
        print(f"Graph error: {e}")
        await sio.emit(
            "ai_status",
            {"message": "Something went wrong on my end. Try again!"},
            room=sid,
        )