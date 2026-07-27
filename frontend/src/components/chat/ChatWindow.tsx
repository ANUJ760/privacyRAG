"use client";

import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

import { Message } from "@/types/message";
import { getModelOptions, sendMessage } from "@/services/chat";
import { useDocument } from "@/providers/DocumentProviders";

export default function ChatWindow() {
  const { collectionName } = useDocument();

  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState("");
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    async function loadModels() {
      try {
        const options = await getModelOptions();
        const savedModel = window.localStorage.getItem("privacyrag:model");
        const model =
          savedModel && options.models.includes(savedModel)
            ? savedModel
            : options.default_model;

        setModels(options.models);
        setSelectedModel(model);
      } catch (error) {
        console.error(error);
      }
    }

    loadModels();
  }, []);

  function handleModelChange(model: string) {
    setSelectedModel(model);
    window.localStorage.setItem("privacyrag:model", model);
  }

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
        model_name: selectedModel || undefined,
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
      <div className="flex items-center justify-between gap-3 border-b border-border bg-[#061624] px-3 py-2">
        <span className="text-[10px] uppercase text-muted-foreground">
          model
        </span>

        <select
          className="min-w-0 border border-border bg-[#071827] px-2 py-1 text-[11px] text-foreground outline-none focus:border-primary"
          disabled={loading || models.length === 0}
          value={selectedModel}
          onChange={(event) => handleModelChange(event.target.value)}
        >
          {models.length === 0 ? (
            <option value="">loading models</option>
          ) : (
            models.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))
          )}
        </select>
      </div>

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
