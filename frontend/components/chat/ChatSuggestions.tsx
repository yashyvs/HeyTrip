"use client";

import { useState } from "react";

type Props = {
  options: string[];

  multiSelect?: boolean;

  onSelect: (text: string) => void;
};

export default function ChatSuggestions({
  options,

  multiSelect,

  onSelect,
}: Props) {
  const [selected, setSelected] = useState<string[]>([]);

  const toggleOption = (item: string) => {
    if (!multiSelect) {
      onSelect(item);

      return;
    }

    if (selected.includes(item)) {
      setSelected((prev) => prev.filter((x) => x !== item));
    } else {
      setSelected((prev) => [...prev, item]);
    }
  };

  return (
    <div
      className="
mt-3
flex
gap-2
flex-wrap
"
    >
      {options.map((option) => (
        <button
          key={option}
          onClick={() => toggleOption(option)}
          className={`
px-4
py-2
rounded-full
border
transition

${selected.includes(option) ? "bg-black text-white" : "bg-white text-black"}
`}
        >
          {option}
        </button>
      ))}

      {multiSelect && selected.length > 0 && (
        <button
          onClick={() => onSelect(selected.join(", "))}
          className="
px-4
py-2
rounded-full
bg-blue-500
text-white
"
        >
          Continue
        </button>
      )}
    </div>
  );
}
