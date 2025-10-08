"use client";

import { useState } from "react";
import ChatList from "./components/ChatList";
import Chat from "./components/Chat";
import { Chat as ChatType } from "./services/chatService";

export default function Home() {
  const [selectedChat, setSelectedChat] = useState<ChatType | null>(null);

  return (
    <div className="min-h-screen bg-black text-white flex">
      <ChatList
        onSelectChat={setSelectedChat}
        selectedChatId={selectedChat?.id}
      />
      <div className="flex-1 flex items-center justify-center">
        {selectedChat ? (
          <Chat chatId={selectedChat.id} />
        ) : (
          <div className="text-neutral-400">
            Selecione ou crie um chat para começar
          </div>
        )}
      </div>
    </div>
  );
}
