"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  onSend: (message: string) => void;
}

export default function ChatInput({
  onSend,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  function handleSend() {
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  }

  return (
    <div className="border-t p-4 space-y-2">
      <Textarea
        placeholder="Ask a question..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <Button onClick={handleSend}>
        Send
      </Button>
    </div>
  );
}