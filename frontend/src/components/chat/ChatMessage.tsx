import Markdown from "react-markdown";
import { Message } from "@/types/message";

interface Props {
  message: Message;
}

export default function ChatMessage({
  message,
}: Props) {
  return (
    <div
      className={`rounded-lg p-4 ${
        message.role === "user"
          ? "bg-blue-100"
          : "bg-gray-100"
      }`}
    >
      <Markdown>{message.content}</Markdown>
    </div>
  );
}