export interface PromptResponse {
  result: string;
  has_plot?: boolean;
  plot_image?: string;
}

export async function sendPrompt(prompt: string): Promise<PromptResponse> {
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
    
    // Se o retorno for apenas uma string (compatibilidade com versão antiga)
    if (typeof data === 'string') {
      return { result: data };
    }
    
    // Se o retorno for um objeto com result
    if (data.result !== undefined) {
      return {
        result: data.result,
        has_plot: data.has_plot || false,
        plot_image: data.plot_image
      };
    }
    
    return { result: "Sem resposta do agente." };
  } catch (error: any) {
    return { result: error.message || "Erro desconhecido ao conectar ao backend." };
  }
}