import { api } from "@/lib/api";
import { UploadResponse } from "@/types/upload";

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<UploadResponse>(
    "/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
} // this function uploads a document to the server using the provided file. It creates a FormData object, appends the file to it, and sends a POST request to the "/upload" endpoint. The response is expected to be of type UploadResponse, which contains information about the uploaded file.
