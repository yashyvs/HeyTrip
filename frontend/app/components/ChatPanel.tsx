"use client";

import type { FormEvent, KeyboardEvent } from "react";
import type { ChatThread } from "../types";
import MessageList from "./MessageList";

interface ChatPanelProps {
  activeThread: ChatThread | null;
  loading: boolean;
  input: string;
  onInputChange: (value: string) => void;
  onSubmit: (event?: FormEvent<HTMLFormElement>) => void;
  onToggleSidebar: () => void;
}

const suggestions = [
  {
    icon: "🏝️",
    title: "Plan a beach getaway",
    prompt: "Plan a 4-day beach trip to Goa for two people.",
  },
  {
    icon: "🏔️",
    title: "Explore the mountains",
    prompt: "Plan a 5-day trip to Manali with sightseeing and activities.",
  },
  {
    icon: "🌆",
    title: "Discover a new city",
    prompt: "Plan a 3-day trip to Jaipur covering its major attractions.",
  },
  {
    icon: "💰",
    title: "Travel on a budget",
    prompt: "Plan a budget-friendly 3-day trip from Delhi for two people.",
  },
];

export default function ChatPanel({
  activeThread,
  loading,
  input,
  onInputChange,
  onSubmit,
  onToggleSidebar,
}: ChatPanelProps) {
  const hasMessages = Boolean(activeThread?.messages.length);

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  }

  function handleSuggestion(prompt: string) {
    onInputChange(prompt);
  }

  return (
    <main className="chat-panel">
      <header className="topbar">
        <div className="topbar-left">
          <button
            className="icon-button menu-button"
            onClick={onToggleSidebar}
            aria-label="Toggle sidebar"
          >
            ☰
          </button>

          <div className="topbar-title">
            <span className="topbar-heading">Trip Planner</span>
            <span className="topbar-status">
              <span className="status-dot" />
              AI travel assistant
            </span>
          </div>
        </div>

        <div className="topbar-badge">
          <span>✦</span> AI powered
        </div>
      </header>

      <section className="chat-body">
        {!hasMessages ? (
          <div className="welcome-screen">
            <div className="welcome-icon">
              <span>✈</span>
            </div>

            <div className="welcome-eyebrow">
              YOUR NEXT ADVENTURE STARTS HERE
            </div>

            <h1>
              Where do you
              <br />
              <span>want to go?</span>
            </h1>

            <p className="welcome-description">
              Tell me what you have in mind. I’ll help you explore destinations,
              discover places to stay, and build an itinerary that fits your
              trip.
            </p>

            <div className="suggestion-grid">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion.title}
                  className="suggestion-card"
                  onClick={() => handleSuggestion(suggestion.prompt)}
                >
                  <span className="suggestion-icon">{suggestion.icon}</span>
                  <span className="suggestion-copy">
                    <span className="suggestion-title">{suggestion.title}</span>
                    <span className="suggestion-description">
                      {suggestion.prompt}
                    </span>
                  </span>
                  <span className="suggestion-arrow">↗</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="conversation-container">
            <MessageList
              messages={activeThread?.messages ?? []}
              loading={loading}
            />
          </div>
        )}
      </section>

      <footer className="composer-area">
        <form
          className="composer"
          onSubmit={(event) => {
            event.preventDefault();
            onSubmit(event);
          }}
        >
          <textarea
            value={input}
            onChange={(event) => onInputChange(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Tell me where you want to go..."
            rows={1}
            aria-label="Your travel message"
            disabled={loading}
          />

          <div className="composer-bottom">
            <span className="composer-hint">
              <span>↵</span> Enter to send · Shift + Enter for a new line
            </span>

            <button
              type="submit"
              className="send-button"
              disabled={loading || !input.trim()}
              aria-label="Send message"
            >
              <span>{loading ? "..." : "Send"}</span>
              {!loading && <span>↑</span>}
            </button>
          </div>
        </form>

        <p className="disclaimer">
          HeyTrip can make mistakes. Verify travel details before booking.
        </p>
      </footer>
    </main>
  );
}
