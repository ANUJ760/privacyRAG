import ChatWindow from "@/components/chat/ChatWindow";
import Navbar from "@/components/layout/navbar";
import Sidebar from "@/components/layout/sidebar";
import UploadCard from "@/components/upload/UploadCard";

export default function Home() {
  return (
    <main className="flex h-screen flex-col overflow-hidden bg-background">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <section className="flex min-w-0 flex-1">
          <div className="w-72 shrink-0 border-r border-border bg-[#071827] p-3">
            <UploadCard />
          </div>

          <div className="min-w-0 flex-1 bg-[#05111f]">
            <ChatWindow />
          </div>
        </section>
      </div>
    </main>
  );
}
