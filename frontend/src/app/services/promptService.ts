interface PromptResponse {
  result: string;
  has_plot: boolean;
}

export async function sendPrompt(prompt: string, chatId: number): Promise<PromptResponse> {
  try {
    const res = await fetch("http://localhost:8000/prompt/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, chat_id: chatId }),
    });
    
    if (!res.ok) {
      throw new Error("Erro ao processar o prompt.");
    }
    
    return await res.json();
  } catch (error: any) {
    return {
      result: error.message || "Erro ao conectar ao backend.",
      has_plot: false
    };
  }
}