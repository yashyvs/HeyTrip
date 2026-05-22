type Day = {
  day: number;

  title: string;

  places: string[];
};

type Props = {
  days: Day[];
};

export default function ItineraryTimeline({ days }: Props) {
  return (
    <div className="space-y-4 mt-4">
      {days.map((d) => (
        <div
          key={d.day}
          className="
bg-white
rounded-2xl
shadow
p-5
border-l-4
border-blue-500
"
        >
          <div
            className="
text-sm
text-gray-500
"
          >
            Day {d.day}
          </div>

          <h2
            className="
font-bold
text-lg
mt-1
"
          >
            {d.title}
          </h2>

          <div
            className="
mt-3
space-y-2
"
          >
            {d.places.map((place) => (
              <div key={place}>📍 {place}</div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
