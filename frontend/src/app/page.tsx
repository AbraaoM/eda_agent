"use client";

import { useState, useRef, useEffect } from "react";
import { sendPrompt } from "./services/promptService";

export default function Home() {
  const [messages, setMessages] = useState<{ role: "user" | "agent"; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setLoading(true);
    setInput("");
    const agentReply = await sendPrompt(input);
    setMessages((msgs) => [
      ...msgs,
      { role: "agent", text: agentReply },
    ]);
    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center font-sans">
      <div className="w-full max-w-2xl flex flex-col h-[80vh] rounded-xl shadow-lg border border-neutral-800 bg-neutral-900">
        {/* Área de mensagens */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-neutral-400">Nenhuma conversa ainda.</div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat ${msg.role === "user" ? "chat-end" : "chat-start"}`}
            >
              <div
                className={`chat-bubble ${
                  msg.role === "user"
                    ? "chat-bubble-primary bg-primary text-white"
                    : "chat-bubble-secondary bg-neutral-800 text-white"
                } whitespace-pre-wrap break-words max-w-xl`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>
        {/* Campo de entrada */}
        <form
          className="p-4 border-t border-neutral-800 bg-neutral-900 flex gap-2 rounded-lg"
          onSubmit={handleSend}
        >
          <input
            type="text"
            className="p-3 input input-bordered w-full bg-neutral-800 text-white placeholder:text-neutral-400 border-neutral-700 focus:outline-none focus:ring-2 focus:ring-primary rounded-lg"
            placeholder="Digite sua mensagem..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            style={{
              minHeight: "3rem",
              fontSize: "1.1rem",
            }}
          />
          <button
            type="submit"
            className="btn btn-primary px-6 rounded-lg shadow-md transition-transform duration-150 hover:scale-105 hover:bg-primary-focus disabled:opacity-60"
            disabled={loading || !input.trim()}
            style={{ minHeight: "3rem", fontWeight: 600, letterSpacing: 1 }}
          >
            {loading ? (
              <span className="loading loading-spinner loading-xs"></span>
            ) : (
              "Enviar"
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
