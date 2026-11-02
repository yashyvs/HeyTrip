"use client";

import type { ChatThread } from "../types";

interface SidebarProps {
  threads: ChatThread[];
  selectedThreadId: string | null;
  isOpen: boolean;
  onNewChat: () => void;
  onSelectChat: (threadId: string) => void;
  onClose: () => void;
}

export default function Sidebar({
  threads,
  selectedThreadId,
  isOpen,
  onNewChat,
  onSelectChat,
  onClose,
}: SidebarProps) {
  return (
    <>
      {isOpen && (
        <button
          className="sidebar-backdrop"
          aria-label="Close sidebar"
          onClick={onClose}
        />
      )}

      <aside className={`sidebar ${isOpen ? "sidebar-open" : ""}`}>
        <div className="sidebar-top">
          <div className="brand">
            <div className="brand-icon">H</div>
            <span>HeyTrip</span>
          </div>

          <button
            className="icon-button mobile-close"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            ✕
          </button>
        </div>

        <button className="new-chat-button" onClick={onNewChat}>
          <span className="new-chat-icon">＋</span>
          <span>New trip</span>
        </button>

        <div className="sidebar-section-title">YOUR CONVERSATIONS</div>

        <div className="thread-list">
          {threads.length === 0 ? (
            <p className="empty-threads">
              Your conversations will appear here.
            </p>
          ) : (
            threads.map((thread) => (
              <button
                key={thread.id}
                className={`thread-item ${
                  selectedThreadId === thread.id ? "thread-active" : ""
                }`}
                onClick={() => {
                  onSelectChat(thread.id);
                  onClose();
                }}
              >
                <span className="thread-icon">◷</span>

                <span className="thread-title">
                  {thread.title || "New trip"}
                </span>
              </button>
            ))
          )}
        </div>

        <div className="sidebar-footer">
          <div className="profile-avatar">H</div>
          <div className="profile-info">
            <span className="profile-name">HeyTrip Explorer</span>
            <span className="profile-subtitle">Your travel companion</span>
          </div>
        </div>
      </aside>
    </>
  );
}
