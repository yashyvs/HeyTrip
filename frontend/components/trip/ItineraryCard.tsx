type Props = {
  day: number;

  title: string;

  activity: string;
};

export default function ItineraryCard({
  day,

  title,

  activity,
}: Props) {
  return (
    <div
      className="
bg-white
rounded-2xl
p-5
shadow
mb-4
"
    >
      <div
        className="
text-sm
text-gray-500
"
      >
        Day {day}
      </div>

      <h2
        className="
font-bold
text-lg
mt-2
"
      >
        {title}
      </h2>

      <p
        className="
text-gray-600
mt-2
"
      >
        {activity}
      </p>
    </div>
  );
}
