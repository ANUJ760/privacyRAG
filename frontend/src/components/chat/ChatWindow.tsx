"use client";

import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

import { Message } from "@/types/message";
import { sendMessage } from "@/services/chat";
import { useDocument } from "@/providers/DocumentProviders";

export default function ChatWindow() {
  const { collectionName } = useDocument();

  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

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
          content: "The document answer could not be generated. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-3 overflow-y-auto p-3">
        {messages.length === 0 && (
          <div className="border border-border bg-[#071827] p-3 text-[12px] text-muted-foreground">
            Upload a PDF, then ask for summaries, clauses, lists, comparisons,
            definitions, or document-specific follow-ups.
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message}
          />
        ))}

        {loading && (
          <div className="mr-auto border border-border bg-[#071827] p-3 text-[12px] text-muted-foreground">
            thinking...
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      <ChatInput
        disabled={loading}
        onSend={handleSend}
      />
    </div>
  );
}
