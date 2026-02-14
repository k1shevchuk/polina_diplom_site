export function cleanText(value: string | null | undefined, fallback = ""): string {
  if (!value) return fallback;
  const cleaned = value.replace(/\uFFFD+/g, "").trim();
  return cleaned || fallback;
}
