"use client";

import { useState } from "react";

export default function Home() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    location: "",
    skills: "",
    resume_text: "",
  });

  const [result, setResult] = useState("");

  const handleSubmit = async () => {
    const query = new URLSearchParams(form).toString();

    const response = await fetch(
      `http://127.0.0.1:8000/submit?${query}`
    );

    const data = await response.json();

    setResult(JSON.stringify(data));
  };

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold mb-4">
        Resume Submission
      </h1>

      {Object.keys(form).map((key) => (
        <input
          key={key}
          className="border p-2 mb-2 block w-full"
          placeholder={key}
          value={(form as any)[key]}
          onChange={(e) =>
            setForm({ ...form, [key]: e.target.value })
          }
        />
      ))}

      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white p-2 mt-2"
      >
        Submit
      </button>

      {result && (
        <div className="mt-4 p-4 border">
          Result: {result}
        </div>
      )}
    </div>
  );
}