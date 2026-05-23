"use client";

import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import ChatSuggestions from "./ChatSuggestions";
import ItineraryTimeline from "@/components/trip/ItineraryTimeline";
import { Message } from "@/types/chat";

type Props = {
  messages: Message[];
  isTyping: boolean; // ← new prop
  onSelect: (text: string) => void;
};

export default function ChatWindow({ messages, isTyping, onSelect }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // ← Auto-scroll every time messages change or typing indicator appears
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-2">
      {messages.map((msg) => (
        <div key={msg.id}>
          {/* ← Pass itinerary data directly instead of msg.days */}
          {msg.type === "itinerary" && msg.itinerary ? (
            <ItineraryTimeline data={msg.itinerary} />
          ) : (
            <ChatMessage message={msg.text} sender={msg.sender} />
          )}

          {msg.options && (
            <ChatSuggestions
              options={msg.options}
              multiSelect={msg.multiSelect}
              onSelect={onSelect}
            />
          )}
        </div>
      ))}

      {/* ← Animated typing indicator */}
      {isTyping && (
        <div className="flex justify-start">
          <div className="bg-gray-200 rounded-2xl px-5 py-3 flex gap-1 items-center">
            <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:0ms]" />
            <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:150ms]" />
            <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:300ms]" />
          </div>
        </div>
      )}

      {/* ← Scroll target */}
      <div ref={bottomRef} />
    </div>
  );
}
