# reverse-lab

A workspace for reverse engineering websites, games and apps with
**[REA: Reverse Engineer Anything](https://github.com/morluto/rea)** (MIT, npm package
`rea-agents`). REA gives Claude (or any MCP agent) and your terminal one toolkit for
browser capture, JavaScript/Electron reconstruction, .NET/Unity assemblies, Android
APKs and native binaries through Ghidra, IDA or Hopper.

## Quick start

```bash
scripts/setup.sh              # installs rea-agents@6.5.0 (needs Node.js 20+)
scripts/setup.sh --ghidra     # optional: JDK 21 + Ghidra 12.1.4 for native games/binaries
source ~/.reverse-lab/env.sh  # after --ghidra, exposes GHIDRA_INSTALL_DIR
rea doctor                    # shows which engines are ready
```

Open this folder in Claude Code. It picks up the `rea` MCP server from `.mcp.json`
(approve it when prompted), and `CLAUDE.md` explains the workflow to it.

## Investigate something

```bash
scripts/new-target.sh websites some-site       # or: games my-game / apps some-app
```

Then ask Claude, for example:

> Using REA, work out how the search on https://some-site.example ranks results.
> Save evidence in targets/websites/some-site and fill in its README.

### Websites
```bash
scripts/browser.sh https://some-site.example                   # prints the target ids
rea analyze-web-bundle http://127.0.0.1:9222 <target_id> --fetch-source-maps --format json
rea inspect-web-page   http://127.0.0.1:9222 <target_id> --include-json-body-shapes --format json
```

### Games
- **Browser / HTML5 / WASM games:** the website workflow above.
- **Unity (Mono) / .NET games:** point REA's managed-code tools at the game's
  `Managed/*.dll` folder.
- **Electron-based games/launchers:** `rea analyze-javascript-application <dir or app.asar> --json`.
- **Native (C/C++, IL2CPP) games:** run `setup.sh --ghidra`, then `rea analyze` / `rea decompile`.

### Apps
Electron/JS desktop apps, .NET apps, Android APKs and native binaries are covered
the same way; see `CLAUDE.md` for the tool-per-target table.

## Layout
```
.mcp.json          REA MCP server for Claude Code (pinned version)
CLAUDE.md          workflow and ground rules for Claude
scripts/           setup.sh, browser.sh, new-target.sh
targets/           one folder per investigation (websites/, games/, apps/)
notes/             cross-target techniques and write-ups
```

## Ground rules
Stick to public websites and software you own or are licensed to inspect. Don't use
this for DRM, licence-check or anti-cheat bypasses, online-game cheats, or copying
someone else's code into a product: understand the idea, then build your own. Check
REA's own [DISCLAIMER](https://github.com/morluto/rea/blob/main/DISCLAIMER.md).
Binaries and raw captures are git-ignored on purpose.
