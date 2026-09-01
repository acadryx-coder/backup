# AI Agent (Termux edition)

Zero-dependency terminal coding agent. Pure Node.js — no native modules,
no npm install required. Built for 32-bit ARM (`armv8l`) Termux where most
prebuilt agent binaries don't run.

## 1. Get the files onto your phone

Easiest path: push this folder to a private GitHub repo from any machine,
then on your phone:

```bash
pkg install git nodejs -y
git clone <your-repo-url> ~/ai
```

Or copy the three files (`agent.js`, `lib/tools.js`, `package.json`) by hand
into `~/ai/` and `~/ai/lib/` using `nano` if you don't want to use git.

## 2. Make it runnable from anywhere

```bash
chmod +x ~/ai/agent.js
ln -s ~/ai/agent.js $PREFIX/bin/agent
```

## 3. Set your OpenRouter key

Get a free key at https://openrouter.ai (Keys → Create Key), then:

```bash
agent --set-key sk-or-your-key-here
```

This saves it to `~/.ai/config.json` so you don't need to export it every session.

Optionally set a default model (defaults to `qwen/qwen3-coder:free`):

```bash
agent --set-model z-ai/glm-4.5-air:free
```

## 4. Use it

```bash
cd ~/some-project
agent
```

Type a task. The agent will:
- Print its reasoning (`💭 ...`) before each step
- Freely read files / list dirs / search without asking
- **Ask for approval** before any `write_file` or `run_command`
- Keep going until it reports a final answer

Type `exit` to quit.

## Notes

- All file operations happen relative to whatever directory you ran `agent`
  from — not `~/ai`. That's what makes the symlink setup work.
- If a free model returns broken JSON occasionally, the agent will nudge it
  to retry — this happens more on smaller free models. Swap models with
  `agent --set-model <name>` if one is consistently unreliable.
- `run_command` has a 60s timeout and a 5MB output cap, mainly to keep
  things sane on a phone.
