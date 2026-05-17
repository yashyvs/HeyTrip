import { Mic, Send } from "lucide-react";

export default function ChatInput() {
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

      <button>
        <Send />
      </button>
    </div>
  );
}
