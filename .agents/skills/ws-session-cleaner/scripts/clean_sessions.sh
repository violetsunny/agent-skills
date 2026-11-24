#!/usr/bin/env bash
# 清理 ws (workspace-cli) 历史会话：删除 time_updated 早于 N 天的 session 及关联数据。
# 数据目录默认 ~/.local/share/workspace-code-prd，可用 WS_DATA_DIR 覆盖。
set -euo pipefail

DATA_DIR="${WS_DATA_DIR:-${HOME}/.local/share/workspace-code-prd}"
DB="${DATA_DIR}/opencode.db"
SDB="${DATA_DIR}/session-search.db"

usage() {
  cat <<'EOF'
用法: clean_sessions.sh --days N (--dry-run | --apply) [--no-backup] [--vacuum]

  --days N     保留最近 N 天的会话（按 session.time_updated 判定），N 为 >=1 的整数
  --dry-run    只统计将被删除的数据量，不做任何修改
  --apply      实际执行删除（默认先备份两个数据库）
  --no-backup  跳过备份（不推荐）
  --vacuum     删除后 VACUUM 两个数据库以回收磁盘空间

环境变量:
  WS_DATA_DIR  覆盖数据目录（默认 ~/.local/share/workspace-code-prd）
EOF
}

DAYS="" MODE="" BACKUP=1 VACUUM=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="${2:---days 缺少数值}"; shift 2 ;;
    --days=*) DAYS="${1#*=}"; shift ;;
    --dry-run) MODE="dry"; shift ;;
    --apply) MODE="apply"; shift ;;
    --no-backup) BACKUP=0; shift ;;
    --vacuum) VACUUM=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "错误: 未知参数 $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${DAYS}" ]]; then
  echo "错误: 必须指定 --days N" >&2; usage; exit 1
fi
if ! [[ "${DAYS}" =~ ^[0-9]+$ ]] || (( DAYS < 1 )); then
  echo "错误: --days 必须是 >=1 的整数，当前值: ${DAYS}" >&2; exit 1
fi
if [[ -z "${MODE}" ]]; then
  echo "错误: 必须指定 --dry-run（预览）或 --apply（执行）" >&2; usage; exit 1
fi

# 默认路径不存在时自动发现唯一候选
if [[ ! -f "${DB}" ]]; then
  FOUND=$(find "${HOME}/.local/share" -maxdepth 2 -name opencode.db 2>/dev/null || true)
  N_FOUND=$(printf '%s\n' "${FOUND}" | grep -c . || true)
  if [[ "${N_FOUND}" == "1" ]]; then
    DB="${FOUND}"
    DATA_DIR=$(dirname "${DB}")
    SDB="${DATA_DIR}/session-search.db"
  else
    echo "错误: 找不到 opencode.db（数据目录: ${DATA_DIR}，自动发现 ${N_FOUND} 个候选）" >&2
    echo "提示: 用 WS_DATA_DIR=<目录> 指定 ws 数据目录" >&2
    exit 1
  fi
fi

command -v sqlite3 >/dev/null || { echo "错误: 需要 sqlite3" >&2; exit 1; }

NOW_MS=$(( $(date +%s) * 1000 ))
CUTOFF=$(( NOW_MS - DAYS * 86400 * 1000 ))
CUTOFF_DATE=$(date -r $(( CUTOFF / 1000 )) '+%Y-%m-%d %H:%M:%S')

q() { sqlite3 "${DB}" "$1"; }

# 每次运行（dry-run/apply）都汇报备份目录占用，提醒用户决定是否清除旧备份
report_backups() {
  local bdir="${DATA_DIR}/backups"
  echo
  echo "---- 备份占用 ----"
  if [[ ! -d "${bdir}" ]]; then
    echo "备份目录: ${bdir}（尚无历史备份）"
    return
  fi
  local n
  n=$(find "${bdir}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | grep -c . || true)
  echo "备份目录: ${bdir}"
  echo "历史备份: ${n} 份，合计 $(du -sh "${bdir}" 2>/dev/null | cut -f1)"
  if (( n > 0 )); then
    du -sh "${bdir}"/*/ 2>/dev/null | sort -k2 | while read -r sz p; do
      echo "  ${sz}	$(basename "${p}")"
    done
    echo "提醒: 请确认对应清理结果无误后决定是否清除旧备份（建议至少保留最近 1 份；由用户决定，agent 不擅自删除）。"
  fi
}

echo "数据目录: ${DATA_DIR}"
echo "保留策略: 保留最近 ${DAYS} 天（删除 time_updated < ${CUTOFF_DATE} 的会话）"
echo

DEL_SES=$(q "SELECT count(*) FROM session WHERE time_updated < ${CUTOFF};")
KEEP_SES=$(q "SELECT count(*) FROM session WHERE time_updated >= ${CUTOFF};")

if [[ "${DEL_SES}" == "0" && "${MODE}" == "dry" ]]; then
  echo "没有需要清理的会话（现有 session: ${KEEP_SES}）。"
  report_backups
  exit 0
fi

DEL_MSG=$(q "SELECT count(*) FROM message WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF});")
DEL_PART=$(q "SELECT count(*) FROM part WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF});")
DEL_TODO=$(q "SELECT count(*) FROM todo WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF});")
DEL_SE=0
if [[ -f "${SDB}" ]]; then
  DEL_SE=$(sqlite3 "${SDB}" "ATTACH '${DB}' AS m; SELECT count(*) FROM search_entry WHERE session_id IN (SELECT id FROM m.session WHERE time_updated < ${CUTOFF});")
fi

echo "将删除 session: ${DEL_SES}（保留 ${KEEP_SES}）"
echo "关联数据: message=${DEL_MSG} part=${DEL_PART} todo=${DEL_TODO} search_entry=${DEL_SE}"
SIZE_BEFORE=$(du -h "${DB}" | cut -f1)
echo "opencode.db 当前大小: ${SIZE_BEFORE}"

if [[ "${MODE}" == "dry" ]]; then
  echo
  echo "[dry-run] 未做任何修改。执行删除请加 --apply。"
  report_backups
  exit 0
fi

echo

# 搜索索引的删除/VACUUM 会触发 FTS5 触发器，而 sqlite3 CLI（含 macOS 系统版）普遍
# 未编译 FTS5 模块，故该步骤统一走 python3 的 sqlite3。预检放在任何删除之前，
# 避免"主库已删、索引删不掉"的半清理状态。
PY=python3
if [[ -f "${SDB}" ]]; then
  if ! command -v "${PY}" >/dev/null 2>&1 \
    || ! "${PY}" -c "import sqlite3; sqlite3.connect(':memory:').execute('CREATE VIRTUAL TABLE _t USING fts5(x)')" >/dev/null 2>&1; then
    echo "错误: 清理搜索索引需要带 FTS5 模块的 python3 sqlite3，未找到，已中止（未修改任何数据）" >&2
    exit 1
  fi
fi

BK=""
if [[ "${DEL_SES}" == "0" ]]; then
  echo "没有超出保留期的 session，跳过主库删除，仅清理搜索索引孤儿记录。"
else
  if [[ "${BACKUP}" == "1" ]]; then
    BK="${DATA_DIR}/backups/session-clean-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "${BK}"
    sqlite3 "${DB}" ".backup '${BK}/opencode.db'"
    if [[ -f "${SDB}" ]]; then
      sqlite3 "${SDB}" ".backup '${BK}/session-search.db'"
    fi
    echo "备份完成: ${BK}"
  else
    echo "警告: 已跳过备份（--no-backup）"
  fi

  MAIN_OUT=$(sqlite3 "${DB}" <<SQL
.timeout 15000
BEGIN IMMEDIATE;
DELETE FROM part WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF}); SELECT 'part=' || changes();
DELETE FROM message WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF}); SELECT 'message=' || changes();
DELETE FROM todo WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF}); SELECT 'todo=' || changes();
DELETE FROM session_entry WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF}); SELECT 'session_entry=' || changes();
DELETE FROM session_share WHERE session_id IN (SELECT id FROM session WHERE time_updated < ${CUTOFF}); SELECT 'session_share=' || changes();
DELETE FROM session WHERE time_updated < ${CUTOFF}; SELECT 'session=' || changes();
COMMIT;
SQL
)
  echo "主库删除: ${MAIN_OUT//$'\n'/ }"
fi

# 孤儿式清理：删除主库中已不存在 session 的索引记录（幂等，可修复历史半清理状态）
if [[ -f "${SDB}" ]]; then
  SEARCH_OUT=$("${PY}" - "${SDB}" "${DB}" <<'PYEOF'
import sqlite3, sys
con = sqlite3.connect(sys.argv[1], timeout=30)
con.execute("ATTACH ? AS m", (sys.argv[2],))
con.execute("BEGIN IMMEDIATE")
n1 = con.execute("DELETE FROM search_entry WHERE session_id NOT IN (SELECT id FROM m.session)").rowcount
n2 = con.execute("DELETE FROM search_progress WHERE session_id NOT IN (SELECT id FROM m.session)").rowcount
con.commit()
con.close()
print(f"search_entry={n1} search_progress={n2}")
PYEOF
)
  echo "搜索索引删除: ${SEARCH_OUT}"
fi

if [[ "${VACUUM}" == "1" ]]; then
  echo "VACUUM 主库中（数据量大时耗时较长）..."
  sqlite3 "${DB}" <<'SQL'
.timeout 30000
VACUUM;
SQL
  if [[ -f "${SDB}" ]]; then
    echo "VACUUM 搜索索引中..."
    "${PY}" -c "import sqlite3,sys; con=sqlite3.connect(sys.argv[1], timeout=60); con.execute('VACUUM'); con.close()" "${SDB}"
  fi
fi

echo
echo "完成。剩余 session: $(q 'SELECT count(*) FROM session;')"
echo "opencode.db 大小: ${SIZE_BEFORE} -> $(du -h "${DB}" | cut -f1)"
if [[ -n "${BK}" ]]; then
  echo "本次新备份: ${BK}"
fi
report_backups
