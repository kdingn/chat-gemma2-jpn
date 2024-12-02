"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState<String>("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    const res = await fetch("/api-gemma2/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });
    if (res.ok && res.body) {
      const reader = res.body.getReader();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = new TextDecoder().decode(value);
        console.log(text);
        setResponse((prev) => prev + text);
      }
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
