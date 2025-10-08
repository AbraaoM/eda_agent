export async function sendPrompt(prompt: string): Promise<string> {
  try {
    const res = await fetch("http://localhost:8000/prompt/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    if (!res.ok) {
      throw new Error("Erro ao processar o prompt.");
    }
    const data = await res.json();
    return data.result ?? "Sem resposta do agente.";
  } catch (error: any) {
    return error.message || "Erro desconhecido ao conectar ao backend.";
  }
}