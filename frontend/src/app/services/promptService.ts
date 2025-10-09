interface PromptResponse {
  result: string;
  has_plot: boolean;
  plot_image?: string;  // Base64 string for plot image
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
    
    const data = await res.json();
    return {
      result: data.result,
      has_plot: data.has_plot,
      plot_image: data.plot_image  // Passando a imagem em base64
    };
  } catch (error: any) {
    return {
      result: error.message || "Erro ao conectar ao backend.",
      has_plot: false
    };
  }
}