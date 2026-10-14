# reverse-lab: guidance for Claude

This repo is a workspace for understanding how software works using REA
(Reverse Engineer Anything, https://github.com/morluto/rea). The `rea` MCP server
is declared in `.mcp.json`; the same tools exist as the `rea` CLI.

## Before starting
- Run `scripts/setup.sh` if `rea --version` is missing. Add `--ghidra` only for native
  binaries (most PC/console games, native desktop apps).
- One question per investigation. Create its folder with
  `scripts/new-target.sh <websites|games|apps> <name>` and fill in its README.

## Picking the tool
| Target | Start with |
|---|---|
| Website / web app | `scripts/browser.sh <url>`, then `rea analyze-web-bundle` / `rea inspect-web-page` |
| Electron or JS desktop app | `rea analyze-javascript-application <app dir or .asar> --json` |
| Unity (Mono) / .NET game or app | REA managed-code tools (REA docs/managed-code-analysis.md) |
| Native game / binary | Ghidra provider (`setup.sh --ghidra`), then `rea analyze` / `rea decompile` |
| Android APK | `rea decode-android-resources`, JADX provider |
| Browser game (WASM) | web tools, then REA's WASM inspection commands |

Run `rea --help` or `rea <command> --help` for the full catalog.

## Rules
- Only analyze websites that are public and software the user owns or has a licence to
  inspect. No DRM, licence-check or anti-cheat bypasses, no cheats for online games,
  no credential capture.
- Do not commit target binaries, captured bundles or proprietary source; keep them
  under `targets/**/bin/` or `targets/**/captures/` (git-ignored). Commit notes,
  small evidence summaries and our own re-implementations.
- When building "our version" of a feature, write it from the findings, not by
  copying decompiled code.
- Always record what the evidence does not prove (the "Limits" section).
