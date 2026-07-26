import { Message } from "./message";

export interface ChatRequest {
  collection_name: string;
  question: string;
  history?: Message[];
}

export interface ChatResponse {
  answer: string;
}
