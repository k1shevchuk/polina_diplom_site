import { describe, expect, it } from "vitest";
import { readdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

function walk(dir: string, out: string[] = []): string[] {
  const entries = readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, out);
      continue;
    }
    if (/\.(vue|ts|css|d\.ts)$/.test(entry.name)) {
      out.push(full);
    }
  }
  return out;
}

describe("source encoding guard", () => {
  it("does not contain replacement character U+FFFD in frontend/src", () => {
    const root = resolve(process.cwd(), "src");
    const files = walk(root);
    const offenders: string[] = [];

    for (const file of files) {
      const text = readFileSync(file, "utf-8");
      if (text.includes("\uFFFD")) {
        offenders.push(file);
      }
    }

    expect(offenders, `Files with U+FFFD: ${offenders.join(", ")}`).toEqual([]);
  });
});
