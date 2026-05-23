export type ItineraryDay = {
  day: number;
  title: string;
  places: string[];
  tip?: string; // ← new field
};

export type ItineraryData = {
  destination: string;
  total_days: number;
  summary: string;
  days: ItineraryDay[];
};

export type Message = {
  id: number;
  text: string;
  sender: "user" | "ai";
  options?: string[];
  multiSelect?: boolean;
  type?: "chat" | "itinerary";
  itinerary?: ItineraryData; // ← was days?: ItineraryDay[], now the full object
};
