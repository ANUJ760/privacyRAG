import Navbar from "@/components/layout/navbar";
import Sidebar from "@/components/layout/sidebar";
import UploadCard from "@/components/upload/UploadCard";

export default function Home() {
  return (
    <main className="h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <section className="flex flex-1 items-center justify-center">
          <UploadCard />
        </section>
      </div>
    </main>
  );
}