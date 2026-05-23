import { io } from "socket.io-client";

const URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export const socket = io(URL, {
  autoConnect: true,
  reconnectionAttempts: 5,
});
