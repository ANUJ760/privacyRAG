import ChatWindow from "@/components/chat/ChatWindow";
import Navbar from "@/components/layout/navbar";
import Sidebar from "@/components/layout/sidebar";
import UploadCard from "@/components/upload/UploadCard";

export default function Home() {
  return (
    <main className="h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <section className="flex flex-1">
          <div className="w-80 border-r p-4">
            <UploadCard />
          </div>

          <div className="flex-1">
            <ChatWindow />
          </div>
        </section>
      </div>
    </main>
  );
}