"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type MessageListProps = {
  messages: Message[];
  loading?: boolean;
};

export default function MessageList({
  messages,
  loading = false,
}: MessageListProps) {
  return (
    <div className="flex flex-col gap-5">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex w-full ${
            message.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div
            className={`max-w-[90%] rounded-2xl px-4 py-3 sm:max-w-[85%] ${
              message.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-900 dark:bg-[#202127] dark:text-gray-100"
            }`}
          >
            {message.role === "user" ? (
              <p className="whitespace-pre-wrap break-words text-sm leading-7">
                {message.content}
              </p>
            ) : (
              <div className="markdown-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    a: ({ ...props }) => (
                      <a {...props} target="_blank" rel="noopener noreferrer" />
                    ),
                    table: ({ ...props }) => (
                      <div className="my-4 w-full overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
                        <table {...props} />
                      </div>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>
        </div>
      ))}

      {loading && (
        <div className="flex justify-start">
          <div className="rounded-2xl bg-gray-100 px-4 py-3 dark:bg-[#202127]">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500" />
              <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500 [animation-delay:150ms]" />
              <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500 [animation-delay:300ms]" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
