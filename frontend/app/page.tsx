"use client";

import { useEffect, useState } from "react";

import ChatInput from "@/components/chat/ChatInput";
import ChatWindow from "@/components/chat/ChatWindow";

import { Message } from "@/types/chat";
import { socket } from "@/services/socket";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,

      text: "Hey 👋 Where are we traveling today?",

      sender: "ai",

      options: ["Goa 🌴", "Bali 🌊", "Delhi 🏙️", "Manali 🏔️"],
    },
  ]);

  useEffect(() => {
    socket.on("ai_status", (data) => {
      const aiMessage = {
        id: Date.now(),

        text: data.message,

        sender: "ai",
      };

      setMessages((prev) => [...prev, aiMessage]);
    });

    return () => {
      socket.off("ai_status");
    };
  }, []);

  const sendMessage = (text: string) => {
    const userMessage = {
      id: Date.now(),

      text,

      sender: "user" as const,
    };

    setMessages((prev) => [...prev, userMessage]);

    socket.emit("user_message", {
      text,
    });
  };

  return (
    <div
      className="
h-screen
flex
flex-col
bg-slate-100
text-black
"
    >
      <div
        className="
bg-white
border-b
shadow-sm
px-6
py-4
"
      >
        <div
          className="
text-2xl
font-bold
text-slate-800
"
        >
          ✈️ HeyTrip
        </div>

        <p
          className="
text-sm
text-gray-500
mt-1
"
        >
          Your AI travel companion
        </p>
      </div>

      <ChatWindow messages={messages} onSelect={sendMessage} />

      <div
        className="
bg-white
border-t
"
      >
        <ChatInput onSend={sendMessage} />
      </div>
    </div>
  );
}
