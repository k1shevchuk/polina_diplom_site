import type { AxiosInstance } from "axios";

export async function uploadSellerImages(
  apiClient: AxiosInstance,
  uploadEndpoint: string,
  files: File[],
): Promise<string[]> {
  const urls: string[] = [];

  for (const file of files) {
    const body = new FormData();
    body.append("file", file);

    const response = await apiClient.post<{ url: string }>(uploadEndpoint, body, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    urls.push(response.data.url);
  }

  return urls;
}
