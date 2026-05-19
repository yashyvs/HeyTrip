"use client";

import ChatInput from "@/components/chat/ChatInput";
import ChatWindow from "@/components/chat/ChatWindow";

import { Message } from "@/types/chat";

import { useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,

      text: "Hey 👋 Where are we traveling today?",

      sender: "ai",
    },
  ]);

  const sendMessage = (text: string) => {
    const userMessage = {
      id: Date.now(),

      text,

      sender: "user" as const,
    };

    setMessages((prev) => [...prev, userMessage]);

    setTimeout(() => {
      const aiReply = {
        id: Date.now() + 1,

        text: "Interesting 👀 Tell me more.",

        sender: "ai" as const,
      };

      setMessages((prev) => [...prev, aiReply]);
    }, 1000);
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
