"use client";

import { useState, useRef, useEffect } from "react";
import { sendPrompt } from "../services/promptService";

interface ChatProps {
  chatId: number;
}

interface Message {
  role: "user" | "agent";
  text: string;
  plot_image?: string;
}

export default function Chat({ chatId }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setLoading(true);
    setInput("");

    try {
      const response = await sendPrompt(input, chatId);
      setMessages((msgs) => [
        ...msgs,
        { 
          role: "agent", 
          text: response.result,
          plot_image: response.has_plot ? response.plot_image : undefined
        }
      ]);
    } catch (error) {
      setMessages((msgs) => [
        ...msgs,
        { role: "agent", text: "Erro ao processar sua mensagem." }
      ]);
    }
    setLoading(false);
  }

  return (
    <div className="h-full flex flex-col rounded-xl shadow-lg border border-neutral-800 bg-neutral-900">
      {/* Área de mensagens */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && !loading && (
          <div className="text-center text-neutral-400">
            Envie uma mensagem para começar a análise do CSV
          </div>
        )}
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`
                max-w-xl px-5 py-3 rounded-2xl shadow
                ${msg.role === "user"
                  ? "bg-primary text-white self-end rounded-br-sm"
                  : "bg-neutral-800 text-white self-start rounded-bl-sm border border-neutral-700"}
                whitespace-pre-wrap break-words
              `}
            >
              <div className="flex items-center gap-2 mb-1">
                {msg.role === "user" ? (
                  <span className="font-semibold text-xs text-primary-content/80">
                    Você
                  </span>
                ) : (
                  <span className="font-semibold text-xs text-secondary-content/80">
                    Agente
                  </span>
                )}
              </div>
              
              <div className="flex flex-col gap-4">
                <span className="text-base">{msg.text}</span>
                {msg.plot_image && (
                  <div className="mt-2">
                    <img
                      src={`data:image/png;base64,${msg.plot_image}`}
                      alt="Visualization plot"
                      className="rounded-lg w-full max-w-2xl h-auto"
                      onError={(e) => {
                        console.error('Error loading image');
                        (e.target as HTMLImageElement).style.display = 'none';
                      }}
                    />
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {/* Loader */}
        {loading && (
          <div className="flex justify-start">
            <div className="max-w-xl px-5 py-3 rounded-2xl shadow bg-neutral-800 text-white self-start rounded-bl-sm border border-neutral-700 flex items-center gap-2">
              <span className="font-semibold text-xs text-secondary-content/80">Agente</span>
              <span className="loading loading-dots loading-md ml-2" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Campo de entrada */}
      <form
        className="p-4 border-t border-neutral-800 bg-neutral-900 flex gap-2 rounded-b-xl"
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
  );
}