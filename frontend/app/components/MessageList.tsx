"use client";

import type { ChatMessage } from "../types";

interface MessageListProps {
  messages: ChatMessage[];
  loading: boolean;
}

export default function MessageList({ messages, loading }: MessageListProps) {
  return (
    <div className="messages-list">
      {messages.map((message, index) => (
        <div
          key={`${index}-${message.role}`}
          className={`message-row ${
            message.role === "user" ? "message-user" : "message-assistant"
          }`}
        >
          {message.role === "assistant" && (
            <div className="message-avatar assistant-avatar">H</div>
          )}

          <div className="message-content">
            <div className="message-author">
              {message.role === "user" ? "You" : "HeyTrip"}
            </div>

            <div className="message-bubble">
              {message.content.split("\n").map((line, lineIndex) => (
                <span key={lineIndex}>
                  {line}
                  {lineIndex < message.content.split("\n").length - 1 && <br />}
                </span>
              ))}
            </div>
          </div>

          {message.role === "user" && (
            <div className="message-avatar user-avatar">Y</div>
          )}
        </div>
      ))}

      {loading && (
        <div className="message-row message-assistant">
          <div className="message-avatar assistant-avatar">H</div>
          <div className="message-content">
            <div className="message-author">HeyTrip</div>
            <div className="message-bubble typing-bubble">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-label">Planning your trip...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
