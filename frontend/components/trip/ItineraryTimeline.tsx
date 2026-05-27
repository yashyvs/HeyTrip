import { ItineraryData } from "@/types/chat";

type Props = {
  data: ItineraryData;
};

export default function ItineraryTimeline({ data }: Props) {
  return (
    <div className="mt-4 mb-2 max-w-lg space-y-4">
      {/* ── Trip header ─────────────────────────────────────────── */}
      <div className="bg-blue-600 text-white rounded-2xl p-5 shadow">
        <div className="text-xl font-bold">✈️ {data.destination}</div>
        <div className="text-blue-100 text-sm mt-1">
          {data.departure_city && `From ${data.departure_city} · `}
          {data.total_days} days · {data.people}{" "}
          {data.people === 1 ? "person" : "people"}
        </div>
        {data.summary && (
          <p className="text-sm mt-2 text-blue-50">{data.summary}</p>
        )}
      </div>

      {/* ── Stay & Transport ────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-3">
        {data.accommodation && (
          <div className="bg-white rounded-2xl shadow p-4">
            <div className="text-xs font-semibold text-purple-500 uppercase mb-1">
              🏨 Stay
            </div>
            <div className="font-semibold text-sm text-gray-800 capitalize">
              {data.accommodation.type}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {data.accommodation.estimated_cost_per_night_inr} / night
            </div>
            {data.accommodation.recommended_areas?.length > 0 && (
              <div className="text-xs text-gray-400 mt-1">
                📍 {data.accommodation.recommended_areas.join(", ")}
              </div>
            )}
          </div>
        )}

        {data.transport && (
          <div className="bg-white rounded-2xl shadow p-4">
            <div className="text-xs font-semibold text-orange-500 uppercase mb-1">
              🛵 Getting around
            </div>
            <div className="font-semibold text-sm text-gray-800 capitalize">
              {data.transport.type}
            </div>
            {data.transport.local_tips && (
              <div className="text-xs text-gray-500 mt-1">
                {data.transport.local_tips}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ── Budget breakdown ────────────────────────────────────── */}
      {data.budget_breakdown && (
        <div className="bg-green-50 border border-green-200 rounded-2xl p-4">
          <div className="text-xs font-semibold text-green-700 uppercase mb-3">
            💰 Budget Breakdown
          </div>
          <div className="space-y-1">
            {Object.entries(data.budget_breakdown).map(([key, value]) => (
              <div key={key} className="flex justify-between text-sm">
                <span className="text-gray-600 capitalize">
                  {key.replace(/_/g, " ")}
                </span>
                <span
                  className={`font-medium ${key === "total_estimated" ? "text-green-700 font-bold" : "text-gray-800"}`}
                >
                  {value}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Day by day ──────────────────────────────────────────── */}
      <div className="space-y-3">
        {data.days.map((d) => (
          <div
            key={d.day}
            className="bg-white rounded-2xl shadow p-4 border-l-4 border-blue-500"
          >
            <div className="text-xs font-semibold text-blue-500 uppercase tracking-wide">
              Day {d.day}
            </div>
            <h2 className="font-bold text-gray-800 text-base mt-1">
              {d.title}
            </h2>

            {/* Places */}
            <div className="mt-3 space-y-1">
              {d.places.map((place) => (
                <div key={place} className="text-sm text-gray-700 flex gap-2">
                  <span>📍</span>
                  <span>{place}</span>
                </div>
              ))}
            </div>

            {/* Food spots ← NEW */}
            {d.food_spots && d.food_spots.length > 0 && (
              <div className="mt-3 space-y-1">
                <div className="text-xs font-semibold text-rose-500 uppercase">
                  🍜 Food
                </div>
                {d.food_spots.map((f) => (
                  <div key={f} className="text-sm text-gray-700 flex gap-2">
                    <span>🍽️</span>
                    <span>{f}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Transport tip ← NEW */}
            {d.transport_tip && (
              <div className="mt-3 text-xs text-orange-700 bg-orange-50 rounded-lg px-3 py-2">
                🛵 {d.transport_tip}
              </div>
            )}

            {/* General tip */}
            {d.tip && (
              <div className="mt-2 text-xs text-amber-700 bg-amber-50 rounded-lg px-3 py-2">
                💡 {d.tip}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
