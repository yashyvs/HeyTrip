import { io, Socket } from "socket.io-client";

const URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

function getUserId(): string {
  if (typeof window === "undefined") return "ssr";
  let id = localStorage.getItem("heytrip_uid");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("heytrip_uid", id);
  }
  return id;
}

// Singleton — only one socket instance ever exists
// Without this, React StrictMode and hot reload create multiple connections
// which is exactly what was showing up in the server logs
declare global {
  var __heytripSocket: Socket | undefined;
}

if (!globalThis.__heytripSocket) {
  globalThis.__heytripSocket = io(URL, {
    autoConnect: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 3000,
    timeout: 180000,
    auth: { user_id: getUserId() },
  });
}

export const socket = globalThis.__heytripSocket;
