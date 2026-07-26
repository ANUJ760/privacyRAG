"use client";

import { useState } from "react";
import { uploadDocument } from "@/services/upload";

export default function UploadCard() {
  const [uploading, setUploading] = useState(false);

  async function handleChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = e.target.files?.[0];

    if (!file) return;

    setUploading(true);

    try {
      const response = await uploadDocument(file);

      console.log(response);

      alert("Upload successful!");
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="space-y-4">
      <input
        type="file"
        accept=".pdf"
        onChange={handleChange}
      />

      {uploading && <p>Uploading...</p>}
    </div>
  );
}