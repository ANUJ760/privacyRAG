"use client";

import { useState } from "react";
import { uploadDocument } from "@/services/upload";
import { useDocument } from "@/providers/DocumentProviders";

export default function UploadCard() {
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  const { collectionName, setCollectionName } = useDocument();

  async function handleChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = e.target.files?.[0];

    if (!file) return;

    setFileName(file.name);
    setUploading(true);

    try {
      const response = await uploadDocument(file);

      setCollectionName(response.collection_name);

      alert("Upload successful!");
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="space-y-3 text-[11px]">
      <div>
        <p className="mb-1 text-[10px] uppercase text-muted-foreground">
          document input
        </p>
        <label className="flex cursor-pointer items-center justify-center border border-dashed border-border bg-[#061624] px-3 py-5 text-center text-primary transition-colors hover:border-primary hover:bg-[#0a2130]">
          <input
            className="sr-only"
            type="file"
            accept=".pdf"
            onChange={handleChange}
          />
          {uploading ? "indexing pdf..." : "select pdf"}
        </label>
      </div>

      <div className="border border-border bg-[#061624] p-2">
        <p className="text-[10px] uppercase text-muted-foreground">file</p>
        <p className="mt-1 break-all text-foreground">{fileName ?? "none"}</p>
      </div>

      <div className="border border-border bg-[#061624] p-2">
        <p className="text-[10px] uppercase text-muted-foreground">
          collection
        </p>
        <p className="mt-1 break-all text-foreground">
          {collectionName ?? "none"}
        </p>
      </div>
    </div>
  );
}
