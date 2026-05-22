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
    },
  ]);

  useEffect(() => {
    socket.on("ai_status", (data) => {
      const msg = {
        id: Date.now(),

        text: data.message,

        sender: "ai" as const,
      };

      setMessages((prev) => [...prev, msg]);
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

    socket.emit("user_message", { text });
  };

  return (
    <div
      className="
h-screen
flex
flex-col
"
    >
      <div
        className="
p-5
text-2xl
font-bold
border-b
"
      >
        ✈️ HeyTrip
      </div>

      <ChatWindow messages={messages} />

      <ChatInput onSend={sendMessage} />
    </div>
  );
}
