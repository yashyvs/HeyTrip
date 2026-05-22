export type ItineraryDay = {
  day: number;

  title: string;

  places: string[];
};

export type Message = {
  id: number;

  text: string;

  sender: "user" | "ai";

  options?: string[];

  multiSelect?: boolean;

  type?: "chat" | "itinerary";

  days?: ItineraryDay[];
};
