"use client";

import { createContext, useContext, useState } from "react";

type DocumentContextType = {
  collectionName: string | null;
  setCollectionName: (name: string | null) => void;
};

const DocumentContext = createContext<DocumentContextType | undefined>(undefined);

export function DocumentProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [collectionName, setCollectionName] = useState<string | null>(null);

  return (
    <DocumentContext.Provider
      value={{ collectionName, setCollectionName }}
    >
      {children}
    </DocumentContext.Provider>
  );
}

export function useDocument() {
  const context = useContext(DocumentContext);

  if (!context) {
    throw new Error("useDocument must be used inside DocumentProvider");
  }

  return context;
}