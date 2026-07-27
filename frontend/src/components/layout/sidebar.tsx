"use client";

import { useDocument } from "@/providers/DocumentProviders";

export default function Sidebar() {
  const { collectionName } = useDocument();

  return (
    <aside className="w-56 shrink-0 border-r border-border bg-[#061624] p-3">
      <h2 className="mb-3 text-[11px] font-semibold uppercase text-primary">
        Documents
      </h2>

      <div className="border border-border bg-[#071827] p-2">
        <p className="text-[10px] uppercase text-muted-foreground">active</p>
        <p className="mt-1 break-all text-[11px] text-foreground">
          {collectionName ?? "No document uploaded."}
        </p>
      </div>
    </aside>
  );
}
