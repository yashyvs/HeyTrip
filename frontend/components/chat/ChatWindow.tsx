"use client";

import ChatMessage from "./ChatMessage";
import ChatSuggestions from "./ChatSuggestions";

import ItineraryTimeline from "@/components/trip/ItineraryTimeline";

import { Message } from "@/types/chat";

type Props = {
  messages: Message[];

  onSelect: (text: string) => void;
};

export default function ChatWindow({
  messages,

  onSelect,
}: Props) {
  return (
    <div
      className="
        flex-1
        overflow-y-auto
        p-6
        space-y-3
        "
    >
      {messages.map((msg) => (
        <div key={msg.id}>
          {msg.type === "itinerary" ? (
            <ItineraryTimeline days={msg.days!} />
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
    </div>
  );
}
