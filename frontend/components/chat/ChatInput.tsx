"use client";

import { Mic, Send } from "lucide-react";
import { useState } from "react";

type Props = {
  onSend: (message: string) => void;
};

export default function ChatInput({ onSend }: Props) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    onSend(input);

    setInput("");
  };

  return (
    <div
      className="
p-4
border-t
flex
gap-3
"
    >
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
        placeholder="Type a message..."
        className="
flex-1
border
rounded-full
px-4
py-3
outline-none
"
      />

      <button>
        <Mic />
      </button>

      <button onClick={handleSend}>
        <Send />
      </button>
    </div>
  );
}
