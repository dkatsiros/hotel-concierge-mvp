import { useEffect, useRef, useState } from "react";
import { createChatSocket } from "../api/client";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const wsRef = useRef<WebSocket | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ws = createChatSocket();
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data) as Message;
      setMessages((prev) => [...prev, data]);
    };

    return () => ws.close();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function send() {
    const text = input.trim();
    if (!text || !wsRef.current) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    wsRef.current.send(JSON.stringify({ content: text }));
    setInput("");
  }

  return (
    <div className="flex flex-1 flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[80%] rounded-lg px-4 py-2 ${
              msg.role === "user"
                ? "ml-auto bg-stone-800 text-white"
                : "mr-auto bg-stone-200 text-stone-800"
            }`}
          >
            {msg.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
        className="flex gap-2 border-t border-stone-200 p-4"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask the concierge..."
          className="flex-1 rounded-lg border border-stone-300 px-4 py-2 outline-none focus:border-stone-500"
        />
        <button
          type="submit"
          className="rounded-lg bg-stone-800 px-6 py-2 text-white hover:bg-stone-700"
        >
          Send
        </button>
      </form>
    </div>
  );
}
