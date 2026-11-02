"use client";

import type { ChatMessage } from "../types";

interface MessageListProps {
  messages: ChatMessage[];
  loading: boolean;
}

export default function MessageList({ messages, loading }: MessageListProps) {
  return (
    <div className="messages-list">
      {messages.map((message, index) => {
        const isUser = message.role === "user";

        const lines = message.content.split("\n");

        return (
          <div
            key={`${index}-${message.role}`}
            className={`message-row ${
              isUser ? "message-user" : "message-assistant"
            }`}
          >
            {!isUser && (
              <div className="message-avatar assistant-avatar">H</div>
            )}

            <div className="message-content">
              <div className="message-author">{isUser ? "You" : "HeyTrip"}</div>

              <div className="message-bubble">
                {lines.map((line, lineIndex) => (
                  <span key={lineIndex}>
                    {line}
                    {lineIndex < lines.length - 1 && <br />}
                  </span>
                ))}
              </div>
            </div>

            {isUser && <div className="message-avatar user-avatar">Y</div>}
          </div>
        );
      })}

      {loading && (
        <div className="message-row message-assistant">
          <div className="message-avatar assistant-avatar">H</div>

          <div className="message-content">
            <div className="message-author">HeyTrip</div>

            <div className="message-bubble typing-bubble">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />

              <span className="typing-label">HeyTrip is thinking...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
