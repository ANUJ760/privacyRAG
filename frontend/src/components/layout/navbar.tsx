export default function Navbar() {
  return (
    <header className="flex h-10 items-center gap-4 border-b border-border bg-[#061624] px-4">
      <div className="flex items-center gap-1.5" aria-hidden="true">
        <span className="h-3 w-3 rounded-full bg-[#ff5f57]" />
        <span className="h-3 w-3 rounded-full bg-[#ffbd2e]" />
        <span className="h-3 w-3 rounded-full bg-[#28c840]" />
      </div>

      <div className="flex min-w-0 flex-1 items-center justify-between gap-3">
        <h1 className="truncate text-[12px] font-bold uppercase tracking-normal text-primary">
          PrivacyRAG
        </h1>
        <span className="hidden text-[10px] uppercase text-muted-foreground sm:block">
          local document console
        </span>
      </div>
    </header>
  );
}
