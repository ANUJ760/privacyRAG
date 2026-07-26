import Navbar from "@/components/layout/navbar";
import Sidebar from "@/components/layout/sidebar";

export default function Home() {
  return (
    <main className="h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <section className="flex-1 flex items-center justify-center">
          <h2 className="text-2xl font-semibold">
            Upload a document to start chatting
          </h2>
        </section>
      </div>
    </main>
  );
}