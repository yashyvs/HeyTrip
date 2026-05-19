"use client";

import { Message } from "@/types/chat";
import ChatMessage from "./ChatMessage";

type Props = {
  messages: Message[];
};

export default function ChatWindow({ messages }: Props) {
  return (
    <div
      className="
flex-1
overflow-y-auto
p-6
"
    >
      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg.text} sender={msg.sender} />
      ))}
    </div>
  );
}
