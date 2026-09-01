import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

// All paths are resolved against the directory the user launched `agent` from,
// NOT the directory this script lives in. That's what makes `~/ai` work as a
// global tool while still operating on whatever project you're standing in.
const cwd = () => process.cwd();
const resolvePath = (p) => path.resolve(cwd(), p);

export const toolDefs = [
  {
    name: "read_file",
    description: "Read the full contents of a file, relative to the current working directory.",
    params: { path: "string" },
    readonly: true,
  },
  {
    name: "write_file",
    description: "Create or overwrite a file with the given content. Creates parent directories if needed.",
    params: { path: "string", content: "string" },
    readonly: false,
  },
  {
    name: "list_dir",
    description: "List files and folders in a directory (non-recursive).",
    params: { path: "string (use '.' for current dir)" },
    readonly: true,
  },
  {
    name: "search_files",
    description: "Search for a text pattern across files under a directory (like grep -r). Skips node_modules and .git.",
    params: { path: "string (dir to search)", pattern: "string" },
    readonly: true,
  },
  {
    name: "run_command",
    description: "Execute a shell command in the current working directory and return its stdout/stderr.",
    params: { command: "string" },
    readonly: false,
  },
];

function safeList(dirPath) {
  const abs = resolvePath(dirPath);
  const entries = fs.readdirSync(abs, { withFileTypes: true });
  return entries
    .map((e) => (e.isDirectory() ? `${e.name}/` : e.name))
    .sort()
    .join("\n");
}

function searchFiles(dirPath, pattern) {
  const abs = resolvePath(dirPath);
  const results = [];
  const skip = new Set(["node_modules", ".git", ".cache"]);

  function walk(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      if (skip.has(e.name)) continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        walk(full);
      } else {
        try {
          const content = fs.readFileSync(full, "utf8");
          content.split("\n").forEach((line, i) => {
            if (line.includes(pattern)) {
              results.push(`${path.relative(cwd(), full)}:${i + 1}: ${line.trim()}`);
            }
          });
        } catch {
          // binary or unreadable file, skip
        }
      }
    }
  }

  walk(abs);
  return results.slice(0, 200).join("\n") || "(no matches)";
}

// Executes a tool call and returns a plain-text result string to feed back to the model.
export function executeTool(name, params) {
  switch (name) {
    case "read_file": {
      const abs = resolvePath(params.path);
      if (!fs.existsSync(abs)) return `ERROR: file not found: ${params.path}`;
      return fs.readFileSync(abs, "utf8");
    }
    case "write_file": {
      const abs = resolvePath(params.path);
      fs.mkdirSync(path.dirname(abs), { recursive: true });
      fs.writeFileSync(abs, params.content ?? "");
      return `OK: wrote ${params.content?.length ?? 0} bytes to ${params.path}`;
    }
    case "list_dir": {
      return safeList(params.path || ".");
    }
    case "search_files": {
      return searchFiles(params.path || ".", params.pattern);
    }
    case "run_command": {
      try {
        const out = execSync(params.command, {
          cwd: cwd(),
          encoding: "utf8",
          timeout: 60_000,
          maxBuffer: 5 * 1024 * 1024,
        });
        return out || "(command produced no output)";
      } catch (err) {
        return `ERROR (exit ${err.status}): ${err.stdout || ""}${err.stderr || err.message}`;
      }
    }
    default:
      return `ERROR: unknown tool "${name}"`;
  }
}
