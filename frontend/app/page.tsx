
"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";

import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";

import type {
  ChatMessage,
  ChatThread,
  PlanTripResponse,
  HistoryResponse,
} from "./types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const THREADS_STORAGE_KEY = "heytrip_threads";
const ACTIVE_THREAD_KEY = "heytrip_active_thread";

function createThread(): ChatThread {
  return {
    id: crypto.randomUUID(),
    title: "New trip",
    messages: [],
  };
}

export default function Home() {
  const [threads, setThreads] = useState<ChatThread[]>([]);
  const [selectedThreadId, setSelectedThreadId] =
    useState<string | null>(null);

  const [input, setInput] = useState("");
  const [loadingThreadId, setLoadingThreadId] =
    useState<string | null>(null);

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isHydrated, setIsHydrated] = useState(false);

  const initialized = useRef(false);

  const activeThread =
    threads.find(
      (thread) => thread.id === selectedThreadId
    ) ?? null;

  const isLoading =
    loadingThreadId === selectedThreadId;

  // --------------------------------------------------
  // LOAD THREADS FROM LOCAL STORAGE
  // --------------------------------------------------

  useEffect(() => {
    if (initialized.current) return;

    initialized.current = true;

    try {
      const savedThreads = localStorage.getItem(
        THREADS_STORAGE_KEY
      );

      const savedActiveThread = localStorage.getItem(
        ACTIVE_THREAD_KEY
      );

      if (savedThreads) {
        const parsed = JSON.parse(
          savedThreads
        ) as ChatThread[];

        if (Array.isArray(parsed) && parsed.length > 0) {
          setThreads(parsed);

          const activeExists = parsed.some(
            (thread) => thread.id === savedActiveThread
          );

          setSelectedThreadId(
            activeExists
              ? savedActiveThread
              : parsed[0].id
          );

          setIsHydrated(true);
          return;
        }
      }
    } catch (error) {
      console.error(
        "Could not load saved threads:",
        error
      );
    }

    const firstThread = createThread();

    setThreads([firstThread]);
    setSelectedThreadId(firstThread.id);
    setIsHydrated(true);
  }, []);

  // --------------------------------------------------
  // SAVE THREADS TO LOCAL STORAGE
  // --------------------------------------------------

  useEffect(() => {
    if (!isHydrated) return;

    localStorage.setItem(
      THREADS_STORAGE_KEY,
      JSON.stringify(threads)
    );

    if (selectedThreadId) {
      localStorage.setItem(
        ACTIVE_THREAD_KEY,
        selectedThreadId
      );
    }
  }, [threads, selectedThreadId, isHydrated]);

  // --------------------------------------------------
  // UPDATE A THREAD
  // --------------------------------------------------

  const updateThread = useCallback(
    (
      threadId: string,
      updater: (thread: ChatThread) => ChatThread
    ) => {
      setThreads((previous) =>
        previous.map((thread) =>
          thread.id === threadId
            ? updater(thread)
            : thread
        )
      );
    },
    []
  );

  // --------------------------------------------------
  // LOAD HISTORY FROM BACKEND
  // --------------------------------------------------

  useEffect(() => {
    if (!isHydrated || !selectedThreadId) return;

    let cancelled = false;

    async function loadHistory() {
      try {
        const response = await fetch(
          `${API_URL}/history/${encodeURIComponent(
            selectedThreadId!
          )}`
        );

        if (!response.ok) {
          throw new Error(
            "Could not load conversation history."
          );
        }

        const data =
          (await response.json()) as HistoryResponse;

        if (cancelled || !data.messages?.length) {
          return;
        }

        updateThread(
          selectedThreadId!,
          (thread) => ({
            ...thread,
            messages: data.messages,
          })
        );
      } catch (error) {
        console.error(
          "History loading error:",
          error
        );
      }
    }

    loadHistory();

    return () => {
      cancelled = true;
    };
  }, [
    selectedThreadId,
    isHydrated,
    updateThread,
  ]);

  // --------------------------------------------------
  // CREATE NEW CHAT
  // --------------------------------------------------

  const createNewChat = useCallback(() => {
    const newThread = createThread();

    setThreads((previous) => [
      newThread,
      ...previous,
    ]);

    setSelectedThreadId(newThread.id);
    setInput("");

    if (
      window.matchMedia("(max-width: 760px)").matches
    ) {
      setSidebarOpen(false);
    }
  }, []);

  // --------------------------------------------------
  // SELECT EXISTING CHAT
  // --------------------------------------------------

  const selectChat = useCallback(
    (threadId: string) => {
      setSelectedThreadId(threadId);
      setInput("");

      if (
        window.matchMedia("(max-width: 760px)").matches
      ) {
        setSidebarOpen(false);
      }
    },
    []
  );

  // --------------------------------------------------
  // SEND MESSAGE
  // --------------------------------------------------

  async function handleSubmit(
    event?: FormEvent<HTMLFormElement>
  ): Promise<void> {
    event?.preventDefault();

    const query = input.trim();
    const threadId = selectedThreadId;

    if (
      !query ||
      !threadId ||
      loadingThreadId
    ) {
      return;
    }

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

      messages: [
        ...thread.messages,
        userMessage,
      ],
    }));

    setInput("");
    setLoadingThreadId(threadId);

    try {
      const response = await fetch(
        `${API_URL}/plan`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            query,
            thread_id: threadId,
          }),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
          errorText ||
            `Request failed with status ${response.status}`
        );
      }

      const data =
        (await response.json()) as PlanTripResponse;

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content:
          data.response ||
          "I couldn't generate a response. Please try again.",
      };

      updateThread(threadId, (thread) => ({
        ...thread,
        messages: [
          ...thread.messages,
          assistantMessage,
        ],
      }));
    } catch (error) {
      console.error("Chat request failed:", error);

      const errorMessage =
        error instanceof Error
          ? error.message
          : "Something went wrong.";

      updateThread(threadId, (thread) => ({
        ...thread,
        messages: [
          ...thread.messages,
          {
            role: "assistant",
            content:
              "Sorry, I couldn't process your request.\n\n" +
              errorMessage +
              "\n\nPlease check whether the backend is running.",
          },
        ],
      }));
    } finally {
      setLoadingThreadId(null);
    }
  }

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  if (!isHydrated) {
    return (
      <div className="app-shell">
        <main className="chat-panel">
          <div className="conversation-container">
            Loading HeyTrip...
          </div>
        </main>
      </div>
    );
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
        onToggleSidebar={() =>
          setSidebarOpen((previous) => !previous)
        }
      />
    </div>
  );
}
