export async function uploadCSV(file: File): Promise<any> {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://localhost:8000/upload-csv/", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao enviar o arquivo CSV.");
    }
    return await res.json();
  } catch (error: any) {
    return { error: error.message || "Erro desconhecido ao conectar ao backend." };
  }
}