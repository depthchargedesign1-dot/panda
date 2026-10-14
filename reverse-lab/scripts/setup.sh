#!/usr/bin/env bash
# Prepares a machine (or a fresh cloud container) for REA work.
#   scripts/setup.sh           install the REA CLI (web, JS/Electron, .NET, GDB work)
#   scripts/setup.sh --ghidra  also install JDK 21 + Ghidra 12.1.x for native/game binaries
set -euo pipefail

REA_VERSION="6.5.0"
GHIDRA_VERSION="12.1.4"
TOOLS_DIR="${REVERSE_LAB_TOOLS:-$HOME/.reverse-lab}"
WANT_GHIDRA=0
[ "${1:-}" = "--ghidra" ] && WANT_GHIDRA=1
log() { echo "[setup] $*"; }

command -v node >/dev/null || { echo "[setup] Node.js is required (v20+)." >&2; exit 1; }
command -v ps >/dev/null || log "warning: no procps 'ps' on PATH; Ghidra/JS analysis needs it (apt-get install procps)."

if [ "$(rea --version 2>/dev/null || true)" != "$REA_VERSION" ]; then
  log "installing rea-agents@$REA_VERSION"
  npm install --global --silent "rea-agents@$REA_VERSION" >/dev/null
fi
log "rea $(rea --version)"

if [ "$WANT_GHIDRA" = 1 ]; then
  mkdir -p "$TOOLS_DIR"
  if ! java -version 2>&1 | grep -q 'version "2[1-9]'; then
    log "installing OpenJDK 21"
    if command -v apt-get >/dev/null; then
      sudo_cmd=""; [ "$(id -u)" = 0 ] || sudo_cmd="sudo"
      $sudo_cmd apt-get update -qq && $sudo_cmd apt-get install -y -qq openjdk-21-jdk-headless >/dev/null
    else
      echo "[setup] Install a 64-bit JDK 21 yourself and set JAVA_HOME." >&2; exit 1
    fi
  fi
  GHIDRA_DIR="$TOOLS_DIR/ghidra_${GHIDRA_VERSION}_PUBLIC"
  if [ ! -d "$GHIDRA_DIR" ]; then
    log "downloading Ghidra $GHIDRA_VERSION"
    url=$(curl -fsSL "https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/tags/Ghidra_${GHIDRA_VERSION}_build" \
      | grep -o '"browser_download_url": *"[^"]*\.zip"' | head -1 | cut -d'"' -f4)
    [ -n "$url" ] || { echo "[setup] Could not find the Ghidra $GHIDRA_VERSION download." >&2; exit 1; }
    curl -fsSL "$url" -o "$TOOLS_DIR/ghidra.zip"
    (cd "$TOOLS_DIR" && unzip -q ghidra.zip && rm ghidra.zip)
  fi
  echo "export GHIDRA_INSTALL_DIR=\"$GHIDRA_DIR\"" > "$TOOLS_DIR/env.sh"
  log "Ghidra ready. Run: source $TOOLS_DIR/env.sh"
fi
