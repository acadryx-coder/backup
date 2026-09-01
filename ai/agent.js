#!/data/data/com.termux/files/usr/bin/node
import readline from "node:readline";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { toolDefs, executeTool } from "./lib/tools.js";

// ---------- tiny colour helpers (no deps) ----------
const c = {
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
};

// ---------- config ----------
const CONFIG_DIR = path.join(os.homedir(), ".ai");
const CONFIG_PATH = path.join(CONFIG_DIR, "config.json");

function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
  }
  return {};
}

function saveConfig(cfg) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
}

let config = loadConfig();

// Handle --set-key / --set-model BEFORE the api-key check below —
// otherwise you can never set a key on a fresh install (chicken-and-egg bug).
const setKeyIdx = process.argv.indexOf("--set-key");
if (setKeyIdx !== -1 && process.argv[setKeyIdx + 1]) {
  config.apiKey = process.argv[setKeyIdx + 1];
  saveConfig(config);
  console.log(c.green(`Saved API key to ${CONFIG_PATH}`));
  process.exit(0);
}

const setModelIdx = process.argv.indexOf("--set-model");
if (setModelIdx !== -1 && process.argv[setModelIdx + 1]) {
  config.model = process.argv[setModelIdx + 1];
  saveConfig(config);
  console.log(c.green(`Default model set to ${config.model}`));
  process.exit(0);
}

const apiKey = process.env.OPENROUTER_API_KEY || config.apiKey;
const model = process.env.AI_MODEL || config.model || "qwen/qwen3-coder:free";

if (!apiKey) {
  console.log(c.red("No OpenRouter API key found."));
  console.log(`Set one with:\n  export OPENROUTER_API_KEY=sk-or-...\nor run:\n  agent --set-key sk-or-...`);
  process.exit(1);
}

// ---------- system prompt / protocol ----------
const toolList = toolDefs
  .map((t) => `- ${t.name}(${JSON.stringify(t.params)}): ${t.description}`)
  .join("\n");

const SYSTEM_PROMPT = `You are a terminal coding agent operating inside the user's project directory.
You can use these tools:
${toolList}

You MUST respond with ONLY a single JSON object, no markdown fences, no prose outside the JSON.

Two possible shapes:

1. To use a tool:
{"thought": "brief reasoning about what to do next", "tool": "<tool_name>", "params": { ... }}

2. To give your final answer to the user (no more tools needed right now):
{"thought": "brief reasoning", "final_answer": "your message to the user"}

Rules:
- Always include "thought".
- Only one tool call per response — you'll get the result and can decide the next step.
- Use write_file and run_command carefully; the user approves each one before it runs.
- Prefer read_file / list_dir / search_files freely to gather context before making changes.
- When a task is complete, respond with final_answer summarizing what you did.
- Keep file edits complete and correct — write_file overwrites the whole file.`;

// ---------- OpenRouter call ----------
async function callModel(messages) {
  const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
      "HTTP-Referer": "https://termux.local/ai-agent",
      "X-Title": "Termux AI Agent",
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.2,
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`OpenRouter error ${res.status}: ${text}`);
  }

  const data = await res.json();
  const content = data.choices?.[0]?.message?.content;
  if (!content) throw new Error("Empty response from model: " + JSON.stringify(data));
  return content;
}

// Models sometimes emit literal newlines/tabs inside JSON string values
// (e.g. a multi-paragraph final_answer) instead of escaping them as \n.
// That's invalid per the JSON spec even though it looks fine to a human,
// and JSON.parse rejects it outright. Walk the text and escape raw control
// characters ONLY while inside a string literal, leaving the surrounding
// JSON structure/whitespace untouched.
function escapeRawControlCharsInStrings(text) {
  let out = "";
  let inString = false;
  let escapeNext = false;
  for (const ch of text) {
    if (escapeNext) {
      out += ch;
      escapeNext = false;
      continue;
    }
    if (ch === "\\") {
      out += ch;
      escapeNext = true;
      continue;
    }
    if (ch === '"') {
      inString = !inString;
      out += ch;
      continue;
    }
    if (inString) {
      if (ch === "\n") { out += "\\n"; continue; }
      if (ch === "\r") { out += "\\r"; continue; }
      if (ch === "\t") { out += "\\t"; continue; }
    }
    out += ch;
  }
  return out;
}

// Strip markdown fences if the model wraps JSON in ```json ... ``` anyway
function parseModelJSON(raw) {
  let text = raw.trim();
  const fenceMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (fenceMatch) text = fenceMatch[1].trim();

  try {
    return JSON.parse(text);
  } catch (e) {
    // retry after repairing unescaped control chars inside strings
    try {
      return JSON.parse(escapeRawControlCharsInStrings(text));
    } catch (e2) {
      return null;
    }
  }
}

// ---------- readline helpers ----------
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((resolve) => rl.question(q, resolve));

const READONLY_TOOLS = new Set(toolDefs.filter((t) => t.readonly).map((t) => t.name));

async function confirmAction(toolName, params) {
  if (READONLY_TOOLS.has(toolName)) return true; // no approval needed for reads
  console.log(c.yellow(`\n⚠ Approve ${toolName}?`));
  console.log(c.dim(JSON.stringify(params, null, 2)));
  const ans = await ask(c.bold("Run it? [y/N] "));
  return ans.trim().toLowerCase() === "y";
}

// ---------- main loop ----------
async function main() {
  console.log(c.cyan(`\nagent — model: ${model}`));
  console.log(c.dim(`cwd: ${process.cwd()}`));
  console.log(c.dim(`type your task, or "exit" to quit\n`));

  const messages = [{ role: "system", content: SYSTEM_PROMPT }];

  while (true) {
    const userInput = await ask(c.bold("\n> "));
    if (!userInput.trim()) continue;
    if (["exit", "quit"].includes(userInput.trim().toLowerCase())) break;

    messages.push({ role: "user", content: userInput });

    // inner loop: keep calling the model until it gives a final_answer
    let steps = 0;
    while (steps < 25) {
      steps++;
      let raw;
      try {
        process.stdout.write(c.dim("thinking...\n"));
        raw = await callModel(messages);
      } catch (err) {
        console.log(c.red(`\n${err.message}`));
        break;
      }

      const parsed = parseModelJSON(raw);
      if (!parsed) {
        console.log(c.red("\nModel did not return valid JSON. Raw output:"));
        console.log(raw);
        messages.push({
          role: "user",
          content: "Your last response was not valid JSON per the required protocol. Respond again with ONLY the JSON object.",
        });
        continue;
      }

      messages.push({ role: "assistant", content: raw });

      if (parsed.thought) {
        console.log(c.dim(`\n💭 ${parsed.thought}`));
      }

      if (parsed.final_answer) {
        console.log(c.green(`\n${parsed.final_answer}`));
        break;
      }

      if (parsed.tool) {
        console.log(c.cyan(`→ ${parsed.tool}`), c.dim(JSON.stringify(parsed.params || {})));
        const approved = await confirmAction(parsed.tool, parsed.params || {});
        let result;
        if (!approved) {
          result = "User declined to run this action.";
          console.log(c.red("Skipped."));
        } else {
          result = executeTool(parsed.tool, parsed.params || {});
          console.log(c.dim(typeof result === "string" ? result.slice(0, 800) : result));
        }
        messages.push({
          role: "user",
          content: `Tool result for ${parsed.tool}:\n${result}`,
        });
        continue;
      }

      // neither tool nor final_answer present
      console.log(c.red("Model response had neither 'tool' nor 'final_answer'."));
      break;
    }
  }

  rl.close();
  console.log(c.dim("\nbye.\n"));
}

main();
