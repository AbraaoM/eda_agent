"use client";

import Chat from "./components/Chat";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center font-sans">
      <Chat />
    </div>
  );
}
