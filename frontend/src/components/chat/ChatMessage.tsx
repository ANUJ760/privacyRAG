import Markdown from "react-markdown";
import { Message } from "@/types/message";

interface Props {
  message: Message;
}

export default function ChatMessage({
  message,
}: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className={`max-w-[85%] border p-3 text-[12px] leading-relaxed ${
        isUser
          ? "ml-auto border-primary/50 bg-[#0f343e] text-[#d7fff2]"
          : "mr-auto border-border bg-[#071827] text-foreground"
      }`}
    >
      <div className="mb-2 text-[10px] uppercase text-muted-foreground">
        {isUser ? "you" : "assistant"}
      </div>
      <Markdown>{message.content}</Markdown>
    </div>
  );
}
