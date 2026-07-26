export interface ChatRequest {
  collection_name: string;
  question: string;
}

export interface ChatResponse {
  answer: string;
}