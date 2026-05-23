"use client";

import { useEffect, useState } from "react";
import ChatInput from "@/components/chat/ChatInput";
import ChatWindow from "@/components/chat/ChatWindow";
import { Message, ItineraryData } from "@/types/chat";
import { socket } from "@/services/socket";

export default function Home() {
  // ← Empty array — welcome message comes from the backend on connect
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    socket.on("ai_status", (data: { message: string }) => {
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { id: Date.now(), text: data.message, sender: "ai" },
      ]);
    });

    socket.on(
      "itinerary_ready",
      (data: { message: string; itinerary: ItineraryData }) => {
        setIsTyping(false);
        setMessages((prev) => [
          ...prev,
          { id: Date.now(), text: data.message, sender: "ai" },
          {
            id: Date.now() + 1,
            text: "",
            sender: "ai",
            type: "itinerary",
            itinerary: data.itinerary,
          },
        ]);
      },
    );

    return () => {
      socket.off("ai_status");
      socket.off("itinerary_ready");
    };
  }, []);

  const sendMessage = (text: string) => {
    setMessages((prev) => [...prev, { id: Date.now(), text, sender: "user" }]);
    setIsTyping(true);
    socket.emit("user_message", { text });
  };

  return (
    <div className="h-screen flex flex-col bg-slate-100 text-black">
      <div className="bg-white border-b shadow-sm px-6 py-4 flex items-center gap-3">
        <div>
          <div className="text-2xl font-bold text-slate-800">✈️ HeyTrip</div>
          <p className="text-sm text-gray-500">Your AI travel companion</p>
        </div>
        <div className="ml-auto flex items-center gap-2 text-sm text-gray-400">
          <span className="w-2 h-2 rounded-full bg-green-400 inline-block" />
          Live
        </div>
      </div>

      <ChatWindow
        messages={messages}
        isTyping={isTyping}
        onSelect={sendMessage}
      />

      <div className="bg-white border-t">
        <ChatInput onSend={sendMessage} disabled={isTyping} />
      </div>
    </div>
  );
}
