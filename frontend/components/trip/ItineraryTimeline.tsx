import { ItineraryData } from "@/types/chat";

type Props = {
  data: ItineraryData; // ← was days: Day[], now the full object
};

export default function ItineraryTimeline({ data }: Props) {
  return (
    <div className="mt-4 mb-2 max-w-lg">
      {/* ← New: blue header card with destination + summary */}
      <div className="bg-blue-600 text-white rounded-2xl p-5 mb-4 shadow">
        <div className="text-xl font-bold">✈️ {data.destination}</div>
        <div className="text-blue-100 text-sm mt-1">{data.total_days} days</div>
        {data.summary && (
          <p className="text-sm mt-2 text-blue-50">{data.summary}</p>
        )}
      </div>

      <div className="space-y-3">
        {data.days.map((d) => (
          <div
            key={d.day}
            className="bg-white rounded-2xl shadow p-4 border-l-4 border-blue-500"
          >
            <div className="text-xs font-semibold text-blue-500 uppercase tracking-wide mb-1">
              Day {d.day}
            </div>
            <h2 className="font-bold text-gray-800 text-base">{d.title}</h2>

            <div className="mt-3 space-y-1">
              {d.places.map((place) => (
                <div key={place} className="text-sm text-gray-700 flex gap-2">
                  <span>📍</span>
                  <span>{place}</span>
                </div>
              ))}
            </div>

            {/* ← New: tip shown in amber callout */}
            {d.tip && (
              <div className="mt-3 text-xs text-amber-700 bg-amber-50 rounded-lg px-3 py-2">
                💡 {d.tip}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
