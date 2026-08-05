import socketio
from fastapi import FastAPI

from graph.workflow import graph
from memory.session_store import sessions

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_timeout=180,
    ping_interval=25,
)

app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)

# Maps socket id → user id (socket id changes every reconnect, user id stays)
sid_to_uid: dict = {}


@sio.event
async def connect(sid, environ, auth):
    auth = auth or {}
    user_id = auth.get("user_id", sid)

    sid_to_uid[sid] = user_id

    if user_id not in sessions:
        sessions[user_id] = {"messages": [], "pending_options": []}
        print(f"New user: {user_id} (sid: {sid})")
        await sio.emit(
            "ai_status",
            {"message": "Hey 👋 Where are we traveling today?", "options": []},
            room=sid,
        )
    else:
        print(f"Reconnected: {user_id} (sid: {sid})")
        msg_count = len(sessions[user_id].get("messages", []))
        if msg_count > 0:
            await sio.emit(
                "ai_status",
                {
                    "message": "Welcome back! 👋 We were in the middle of planning your trip. What were you saying?",
                    "options": sessions[user_id].get("pending_options", []),
                },
                room=sid,
            )
        else:
            await sio.emit(
                "ai_status",
                {"message": "Hey 👋 Where are we traveling today?", "options": []},
                room=sid,
            )


@sio.event
async def disconnect(sid):
    uid = sid_to_uid.pop(sid, None)
    # Do NOT delete sessions[uid] — user may reconnect and we want to restore their session
    print(f"Disconnected sid: {sid} (user: {uid})")


@sio.event
async def user_message(sid, data):
    user_id = sid_to_uid.get(sid, sid)
    session = sessions.get(user_id)

    if not session:
        session = {"messages": [], "pending_options": []}
        sessions[user_id] = session

    text = data.get("text", "").strip()
    if not text:
        return

    session["messages"].append(f"User: {text}")
    session["pending_options"] = []

    try:
        # ainvoke instead of invoke — server stays responsive during LLM call
        result = await graph.ainvoke(session)
        session.update(result)
        sessions[user_id] = session

        last_msg = result["messages"][-1]
        display_msg = last_msg.removeprefix("AI: ")
        options = result.get("pending_options", [])

        if result.get("itinerary") and result.get("itinerary_done"):
            await sio.emit(
                "itinerary_ready",
                {"message": display_msg, "itinerary": result["itinerary"]},
                room=sid,
            )
        else:
            await sio.emit(
                "ai_status",
                {"message": display_msg, "options": options},
                room=sid,
            )

    except Exception as e:
        print(f"Graph error for {user_id}: {e}")
        await sio.emit(
            "ai_status",
            {
                "message": "⏳ The AI model is still warming up — usually takes under 60 seconds on first use. Try sending your message again!",
                "options": [],
            },
            room=sid,
        )