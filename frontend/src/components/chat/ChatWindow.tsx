"use client";

import { useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

import { Message } from "@/types/message";
import { sendMessage } from "@/services/chat";
import { useDocument } from "@/providers/DocumentProviders";

export default function ChatWindow() {
  const { collectionName } = useDocument();

  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(question: string) {
    if (!collectionName) {
      alert("Please upload a document first.");
      return;
    }

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    const history = messages;

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await sendMessage({
        collection_name: collectionName,
        question,
        history,
      });

      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message}
          />
        ))}

        {loading && <p>Thinking...</p>}
      </div>

      <ChatInput onSend={handleSend} />
    </div>
  );
}
