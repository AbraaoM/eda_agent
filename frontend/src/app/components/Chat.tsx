"use client";

import { useState, useRef, useEffect } from "react";
import { sendPrompt, PromptResponse } from "../services/promptService";

interface Message {
  role: "user" | "agent";
  text: string;
  hasPlot?: boolean;
  plotImage?: string;
}

export default function Chat() {
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
    
    const userMsg: Message = { role: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setLoading(true);
    setInput("");
    
    const response: PromptResponse = await sendPrompt(input);
    
    const agentMsg: Message = {
      role: "agent",
      text: response.result,
      hasPlot: response.has_plot,
      plotImage: response.plot_image
    };
    
    setMessages((msgs) => [...msgs, agentMsg]);
    setLoading(false);
  }

  return (
    <div className="w-full max-w-2xl flex flex-col h-[80vh] rounded-xl shadow-lg border border-neutral-800 bg-neutral-900">
      {/* Área de mensagens */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && !loading && (
          <div className="text-center text-neutral-400">Nenhuma conversa ainda.</div>
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
              style={{
                marginBottom: idx < messages.length - 1 ? "0.5rem" : 0,
                marginTop: idx > 0 && messages[idx - 1].role !== msg.role ? "0.5rem" : 0,
              }}
            >
              <div className="flex items-center gap-2 mb-1">
                {msg.role === "user" ? (
                  <>
                    <span className="font-semibold text-xs text-primary-content/80">Você</span>
                    <span className="i-mdi-account-circle text-xl" />
                  </>
                ) : (
                  <>
                    <span className="i-mdi-robot text-xl" />
                    <span className="font-semibold text-xs text-secondary-content/80">Agente</span>
                  </>
                )}
              </div>
              <span className="text-base">{msg.text}</span>
              {msg.hasPlot && msg.plotImage && (
                <div className="mt-3">
                  <img 
                    src={`data:image/png;base64,${msg.plotImage}`}
                    alt="Gráfico gerado"
                    className="rounded-lg shadow-md max-w-full h-auto border border-neutral-600"
                    style={{ maxHeight: '400px' }}
                  />
                </div>
              )}
            </div>
          </div>
        ))}
        {/* Loader */}
        {loading && (
          <div className="flex justify-start">
            <div className="max-w-xl px-5 py-3 rounded-2xl shadow bg-neutral-800 text-white self-start rounded-bl-sm border border-neutral-700 flex items-center gap-2">
              <span className="i-mdi-robot text-xl" />
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