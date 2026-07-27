import { api } from "@/lib/api";
import { ChatRequest, ChatResponse, ModelOptionsResponse } from "@/types/chat";

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await api.post<ChatResponse>(
    "/chat",
    request
  );

  return response.data;
}

export async function getModelOptions(): Promise<ModelOptionsResponse> {
  const response = await api.get<ModelOptionsResponse>("/chat/models");

  return response.data;
}
