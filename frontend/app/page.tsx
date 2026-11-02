"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import type { ChatMessage, ChatThread, PlanTripResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

function createThread(): ChatThread {
  return {
    id: crypto.randomUUID(),
    title: "New trip",
    messages: [],
  };
}

export default function Home() {
  const [threads, setThreads] = useState<ChatThread[]>([]);
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [loadingThreadId, setLoadingThreadId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const initialized = useRef(false);

  const activeThread =
    threads.find((thread) => thread.id === selectedThreadId) ?? null;

  const isLoading = loadingThreadId === selectedThreadId;

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    const firstThread = createThread();
    setThreads([firstThread]);
    setSelectedThreadId(firstThread.id);
  }, []);

  const createNewChat = useCallback(() => {
    const newThread = createThread();

    setThreads((previous) => [newThread, ...previous]);
    setSelectedThreadId(newThread.id);
    setInput("");

    if (window.matchMedia("(max-width: 760px)").matches) {
      setSidebarOpen(false);
    }
  }, []);

  const selectChat = useCallback((threadId: string) => {
    setSelectedThreadId(threadId);
    setInput("");
  }, []);

  const updateThread = useCallback(
    (threadId: string, updater: (thread: ChatThread) => ChatThread) => {
      setThreads((previous) =>
        previous.map((thread) =>
          thread.id === threadId ? updater(thread) : thread,
        ),
      );
    },
    [],
  );

  async function handleSubmit(
    event?: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event?.preventDefault();

    const query = input.trim();
    const threadId = selectedThreadId;

    if (!query || !threadId || loadingThreadId) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: query,
    };

    updateThread(threadId, (thread) => ({
      ...thread,
      title:
        thread.messages.length === 0
          ? query.length > 32
            ? `${query.slice(0, 32)}…`
            : query
          : thread.title,
      messages: [...thread.messages, userMessage],
    }));

    setInput("");
    setLoadingThreadId(threadId);

    try {
      const response = await fetch(`${API_URL}/plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          thread_id: threadId,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          errorText || `Request failed with status ${response.status}`,
        );
      }

      const data = (await response.json()) as PlanTripResponse;

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content:
          data.response || "I couldn't generate a response. Please try again.",
      };

      updateThread(threadId, (thread) => ({
        ...thread,
        messages: [...thread.messages, assistantMessage],
      }));
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Something went wrong while planning your trip.";

      updateThread(threadId, (thread) => ({
        ...thread,
        messages: [
          ...thread.messages,
          {
            role: "assistant",
            content: `Sorry, I couldn't plan your trip right now.\n\n${errorMessage}\n\nPlease check that the backend is running and try again.`,
          },
        ],
      }));
    } finally {
      setLoadingThreadId(null);
    }
  }

  return (
    <div className="app-shell">
      <Sidebar
        threads={threads}
        selectedThreadId={selectedThreadId}
        isOpen={sidebarOpen}
        onNewChat={createNewChat}
        onSelectChat={selectChat}
        onClose={() => setSidebarOpen(false)}
      />

      <ChatPanel
        activeThread={activeThread}
        loading={isLoading}
        input={input}
        onInputChange={setInput}
        onSubmit={handleSubmit}
        onToggleSidebar={() => setSidebarOpen((previous) => !previous)}
      />
    </div>
  );
}
