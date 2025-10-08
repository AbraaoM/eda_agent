"use client";

import { useState, useEffect } from "react";
import { Chat, listChats, createChat } from "../services/chatService";

interface ChatListProps {
  onSelectChat: (chat: Chat) => void;
  selectedChatId?: number;
}

export default function ChatList({ onSelectChat, selectedChatId }: ChatListProps) {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [chatName, setChatName] = useState("");

  useEffect(() => {
    loadChats();
  }, []);

  async function loadChats() {
    try {
      const chatList = await listChats();
      setChats(chatList);
    } catch (error) {
      console.error("Erro ao carregar chats:", error);
    }
  }

  async function handleCreateChat(e: React.FormEvent) {
    e.preventDefault();
    if (!uploadFile) return;

    setLoading(true);
    try {
      const newChat = await createChat(uploadFile, chatName || undefined);
      setChats([...chats, newChat]);
      setUploadFile(null);
      setChatName("");
    } catch (error) {
      console.error("Erro ao criar chat:", error);
    }
    setLoading(false);
  }

  return (
    <div className="w-64 bg-neutral-900 p-4 border-r border-neutral-800 flex flex-col gap-4">
      <h2 className="text-lg font-semibold text-white">Seus Chats</h2>
      
      {/* Lista de Chats */}
      <div className="flex-1 overflow-y-auto">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelectChat(chat)}
            className={`w-full text-left p-3 rounded-lg mb-2 transition-colors ${
              selectedChatId === chat.id
                ? "bg-primary text-white"
                : "hover:bg-neutral-800 text-neutral-300"
            }`}
          >
            <div className="font-medium">{chat.name || `Chat ${chat.id}`}</div>
            <div className="text-xs opacity-70">{chat.csv_file?.filename}</div>
          </button>
        ))}
      </div>

      {/* Formulário de Novo Chat */}
      <form onSubmit={handleCreateChat} className="space-y-3">
        <input
          type="text"
          placeholder="Nome do chat (opcional)"
          value={chatName}
          onChange={(e) => setChatName(e.target.value)}
          className="input input-bordered w-full bg-neutral-800"
        />
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
          className="file-input file-input-bordered w-full bg-neutral-800"
        />
        <button
          type="submit"
          disabled={!uploadFile || loading}
          className="btn btn-primary w-full"
        >
          {loading ? (
            <span className="loading loading-spinner loading-xs"></span>
          ) : (
            "Criar Chat"
          )}
        </button>
      </form>
    </div>
  );
}