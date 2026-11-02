export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  role: MessageRole;
  content: string;
}

export interface ChatThread {
  id: string;
  title: string;
  messages: ChatMessage[];
}

export interface PlanTripResponse {
  thread_id: string;
  query: string;
  response: string;
}
