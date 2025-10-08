export interface Chat {
  id: number;
  name: string;
  created_at: string;
  csv_file: {
    filename: string;
    filepath: string;
  };
}

export async function createChat(file: File, name?: string): Promise<Chat> {
  const formData = new FormData();
  formData.append("file", file);
  if (name) {
    formData.append("name", name);
  }

  const res = await fetch("http://localhost:8000/chats/", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    throw new Error("Erro ao criar chat.");
  }
  return res.json();
}

export async function listChats(): Promise<Chat[]> {
  const res = await fetch("http://localhost:8000/chats/");
  if (!res.ok) {
    throw new Error("Erro ao listar chats.");
  }
  return res.json();
}

export async function getChat(id: number): Promise<Chat> {
  const res = await fetch(`http://localhost:8000/chats/${id}`);
  if (!res.ok) {
    throw new Error("Erro ao buscar chat.");
  }
  return res.json();
}