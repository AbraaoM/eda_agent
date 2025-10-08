"use client";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center font-sans">
      <div className="w-full max-w-2xl flex flex-col h-[80vh] rounded-xl shadow-lg border border-neutral-800 bg-neutral-900">
        {/* Área de mensagens */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <div className="text-center text-neutral-400">Nenhuma conversa ainda.</div>
        </div>
        {/* Campo de entrada */}
        <form className="p-4 border-t border-neutral-800 bg-neutral-900 flex gap-2 rounded-lg">
          <input
            type="text"
            className="p-3 input input-bordered w-full bg-neutral-800 text-white placeholder:text-neutral-400 border-neutral-700 focus:outline-none focus:ring-2 focus:ring-primary rounded-lg"
            placeholder="Digite sua mensagem..."
            disabled
            style={{
              minHeight: "3rem",
              fontSize: "1.1rem",
            }}
          />
          <button
            type="submit"
            className="btn btn-primary px-6 rounded-lg shadow-md transition-transform duration-150 hover:scale-105 hover:bg-primary-focus disabled:opacity-60"
            disabled
            style={{ minHeight: "3rem", fontWeight: 600, letterSpacing: 1 }}
          >
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}
