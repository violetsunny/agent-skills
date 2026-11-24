#!/usr/bin/env bash
# collect_sessions.sh — 收集指定根目录下所有项目的 ws session 记录，筛选 dev-paradigm / dev-commit 相关会话并导出文本
# 用法: collect_sessions.sh [--root PATH] [--since DAYS] [--out DIR]
# 环境变量: WS_DB 可覆盖数据库路径
set -euo pipefail

ROOT="/Users/kangll13/aiot/java-code/aiot-robot/"
SINCE_DAYS=0
OUT="/tmp/command-retro-$(date +%Y%m%d-%H%M%S)"
DB="${WS_DB:-$HOME/.local/share/workspace-code-prd/opencode.db}"

while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="$2"; shift 2;;
    --since) SINCE_DAYS="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

command -v sqlite3 >/dev/null 2>&1 || { echo "MISSING: sqlite3"; exit 1; }
[ -f "$DB" ] || { echo "MISSING DB: $DB"; exit 1; }
[ -d "$ROOT" ] || { echo "MISSING ROOT: $ROOT"; exit 1; }

SINCE_CLAUSE=""
if [ "$SINCE_DAYS" -gt 0 ] 2>/dev/null; then
  SINCE_MS=$(( ( $(date +%s) - SINCE_DAYS * 86400 ) * 1000 ))
  SINCE_CLAUSE="AND s.time_created >= ${SINCE_MS}"
fi

mkdir -p "${OUT}/matched"

sqlite3 -separator '|' "$DB" \
  "SELECT s.id, s.directory, datetime(s.time_created/1000,'unixepoch','localtime'), s.title FROM session s WHERE s.directory LIKE '${ROOT}%' ${SINCE_CLAUSE} ORDER BY s.time_created DESC" \
  > "${OUT}/sessions-index.txt"

sqlite3 "$DB" \
  "SELECT DISTINCT p.session_id FROM part p JOIN session s ON s.id = p.session_id WHERE s.directory LIKE '${ROOT}%' ${SINCE_CLAUSE} AND (p.data LIKE '%dev-paradigm%' OR p.data LIKE '%dev-commit%')" \
  > "${OUT}/matched-ids.txt"

while IFS= read -r sid; do
  [ -z "$sid" ] && continue
  {
    sqlite3 -separator ' | ' "$DB" \
      "SELECT '=== SESSION ' || s.id, '=== DIR ' || s.directory, '=== TIME ' || datetime(s.time_created/1000,'unixepoch','localtime'), '=== TITLE ' || s.title FROM session s WHERE s.id = '${sid}'"
    sqlite3 "$DB" \
      "SELECT char(10) || '----[' || COALESCE(json_extract(m.data,'\$.role'),'?') || ' @' || datetime(m.time_created/1000,'unixepoch','localtime') || ']----' || char(10) || COALESCE(json_extract(p.data,'\$.text'),'') FROM message m JOIN part p ON p.message_id = m.id WHERE p.session_id = '${sid}' AND json_extract(p.data,'\$.type') = 'text' ORDER BY m.time_created, p.time_created"
  } > "${OUT}/matched/${sid}.txt"
done < "${OUT}/matched-ids.txt"

TOTAL=$(wc -l < "${OUT}/sessions-index.txt" | tr -d ' ')
MATCHED=$(wc -l < "${OUT}/matched-ids.txt" | tr -d ' ')
echo "OUT=${OUT}"
echo "TOTAL=${TOTAL} MATCHED=${MATCHED}"
du -sh "${OUT}/matched" 2>/dev/null
