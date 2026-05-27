export type ItineraryDay = {
  day: number;
  title: string;
  places: string[];
  food_spots?: string[]; // ← NEW
  transport_tip?: string; // ← NEW
  tip?: string;
};

export type ItineraryData = {
  destination: string;
  departure_city?: string; // ← NEW
  total_days: number;
  people?: number; // ← NEW
  summary: string;
  accommodation?: {
    // ← NEW
    type: string;
    estimated_cost_per_night_inr: string;
    recommended_areas: string[];
  };
  transport?: {
    // ← NEW
    type: string;
    local_tips: string;
  };
  budget_breakdown?: Record<string, string>; // ← NEW
  days: ItineraryDay[];
};

export type Message = {
  id: number;
  text: string;
  sender: "user" | "ai";
  options?: string[];
  multiSelect?: boolean;
  type?: "chat" | "itinerary";
  itinerary?: ItineraryData;
};
