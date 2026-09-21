#!/usr/bin/env bash
set -u
miss=0
for s in diagram-design ui-ux-pro-max; do
  if [ -d "$HOME/.agents/skills/$s" ]; then echo "[OK] $s"; else echo "[MISS] $s"; miss=1; fi
done
exit $miss
