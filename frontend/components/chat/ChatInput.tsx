"use client";

import { Send } from "lucide-react";
import { useState } from "react";

type Props = {
  onSend: (message: string) => void;
  disabled?: boolean; // ← new prop
};

export default function ChatInput({ onSend, disabled }: Props) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim() || disabled) return;
    onSend(input.trim());
    setInput("");
  };

  return (
    <div className="p-4 flex gap-3 items-center">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSend();
        }}
        disabled={disabled}
        // ← Placeholder changes while waiting
        placeholder={disabled ? "HeyTrip is thinking..." : "Type a message..."}
        className="flex-1 border rounded-full px-4 py-3 outline-none focus:ring-2
                   focus:ring-blue-400 disabled:bg-gray-50 disabled:text-gray-400 transition"
      />
      <button
        onClick={handleSend}
        disabled={disabled || !input.trim()}
        // ← Button goes gray when disabled
        className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white
                   w-10 h-10 rounded-full flex items-center justify-center transition"
      >
        <Send size={18} />
      </button>
    </div>
  );
}
