"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState<String>("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });
    if (response.ok) {
      const data = await response.json();
      setResponse(data.message);
    }
  };

  return (
    <div>
      <div>You:</div>
      <div>&gt; {message}</div>
      <div>Gemma2:</div>
      <div>&gt; {response}</div>
      <br />
      <div>
        <textarea onChange={(e) => setMessage(e.target.value)} />
      </div>
      <div>
        <button onClick={sendMessage}>send message</button>
      </div>
    </div>
  );
}
