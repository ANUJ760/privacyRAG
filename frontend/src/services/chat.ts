import { api } from "@/lib/api";
import { ChatRequest, ChatResponse } from "@/types/chat";

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await api.post<ChatResponse>(
    "/chat",
    request
  );

  return response.data;
}