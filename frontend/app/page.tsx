import ChatInput from "@/components/chat/ChatInput";
import ChatWindow from "@/components/chat/ChatWindow";

export default function Home() {
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

      <ChatWindow />

      <ChatInput />
    </div>
  );
}
