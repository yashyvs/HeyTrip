type Props = {
  message: string;
  sender: "user" | "ai";
};

export default function ChatMessage({ message, sender }: Props) {
  return (
    <div
      className={`flex ${sender === "user" ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`
        max-w-[70%]
        rounded-2xl
        p-4
        my-2
        
        ${
          sender === "user"
            ? "bg-blue-500 text-white"
            : "bg-gray-200 text-black"
        }
        `}
      >
        {message}
      </div>
    </div>
  );
}
