import ChatMessage from "./ChatMessage";

const messages = [
  {
    sender: "ai",
    message: "Hey 👋 Where are we traveling today?",
  },
];

export default function ChatWindow() {
  return (
    <div
      className="
      flex-1
      overflow-y-auto
      p-6
      "
    >
      {messages.map((msg, index) => (
        <ChatMessage
          key={index}
          message={msg.message}
          sender={msg.sender as "user" | "ai"}
        />
      ))}
    </div>
  );
}
