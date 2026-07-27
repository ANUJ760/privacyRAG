"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({
  onSend,
  disabled = false,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  function handleSend() {
    if (disabled || !message.trim()) return;

    onSend(message);
    setMessage("");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key !== "Enter" || e.shiftKey) return;

    e.preventDefault();
    handleSend();
  }

  return (
    <div className="space-y-2 border-t border-border bg-[#061624] p-3">
      <Textarea
        className="max-h-32 resize-none bg-[#071827]"
        placeholder="ask about the uploaded document..."
        value={message}
        disabled={disabled}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <Button
        className="w-full uppercase"
        disabled={disabled || !message.trim()}
        onClick={handleSend}
      >
        {disabled ? "thinking" : "send"}
      </Button>
    </div>
  );
}
