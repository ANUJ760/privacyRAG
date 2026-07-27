import { Message } from "./message";

export interface ChatRequest {
  collection_name: string;
  question: string;
  history?: Message[];
  model_name?: string;
}

export interface ChatResponse {
  answer: string;
}

export interface ModelOptionsResponse {
  default_model: string;
  models: string[];
}
