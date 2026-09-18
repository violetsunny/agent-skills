#!/bin/bash
# 模块 5 阶段二：合并回填 + 生成文档 + 更新快照 + 验证报告
# 用法: m5_render.sh   （须先跑 m5_extract.sh，且 sub agent 已写好 /tmp/zh/out_NN.json）
# 产出: docs/skills-overview.md（整体重写）、docs/.skills-overview-mtimes.json（快照重建，
#       快照中有但磁盘已删的条目自然移除）
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

RECORDS="$WORK_DIR/m5_records.jsonl"
IDMAP="$WORK_DIR/m5_idmap.jsonl"
OUT_ALL="$WORK_DIR/m5_out_all.json"
FINAL="$WORK_DIR/m5_final.jsonl"
DOC="$KB_DOCS/skills-overview.md"
SNAP="$KB_DOCS/.skills-overview-mtimes.json"
ZH_DIR="/tmp/zh"
SEP="@|SEP|@"

[ -f "$RECORDS" ] || { echo "[FATAL] 先运行 m5_extract.sh"; exit 1; }
mkdir -p "$KB_DOCS"

# 1) 合并 sub agent 翻译产出（逐批校验合法性）
if ls "$ZH_DIR"/out_*.json >/dev/null 2>&1; then
  for f in "$ZH_DIR"/out_*.json; do
    jq -e 'type=="array"' "$f" >/dev/null 2>&1 || { echo "[FATAL] out 文件非法 JSON 数组: $f"; exit 1; }
  done
  jq -s 'add // []' "$ZH_DIR"/out_*.json > "$OUT_ALL"
else
  echo '[]' > "$OUT_ALL"
fi
if [ -f "$IDMAP" ]; then jq -s '.' "$IDMAP" > "$WORK_DIR/m5_idmap_arr.json"; else echo '[]' > "$WORK_DIR/m5_idmap_arr.json"; fi

# 2) 回填：cached 用缓存 zh，dirty 查 (name,desc)→zh 映射
jq -c -s --slurpfile ima "$WORK_DIR/m5_idmap_arr.json" --slurpfile oa "$OUT_ALL" --arg sep "$SEP" '
  ($ima[0] // []) as $im |
  ($oa[0] // []) as $oa2 |
  ($oa2 | map({key:(.id|tostring), value:(.zh // "")}) | from_entries) as $id2zh |
  (reduce $im[] as $e ({};
    ($id2zh[($e.id|tostring)] // "") as $z |
    if ($z|length) > 0 then .[($e.name + $sep + $e.desc)] = $z else . end)) as $nd2zh |
  .[] |
  if .cached and ((.zh|length) > 0) then . + {zh_final: .zh}
  else . + {zh_final: ($nd2zh[(.name + $sep + .desc)] // "")}
  end
' "$RECORDS" > "$FINAL"

# 3) 验证：zh 非空 / 无换行 / ≤500 字；缺失即失败可见，不静默生成残缺文档
n_total=$(wc -l < "$FINAL" | tr -d ' ')
n_missing=$(jq -s '[.[]|select((.zh_final|length)==0)]|length' "$FINAL")
n_newline=$(jq -s '[.[]|select(.zh_final|test("\n"))]|length' "$FINAL")
n_over=$(jq -s '[.[]|select((.zh_final|length)>500)]|length' "$FINAL")
if [ "$n_missing" -gt 0 ]; then
  echo "[M5-MISS-ZH] $n_missing 条缺翻译（id 缺漏或 out 未写全），清单："
  jq -r 'select((.zh_final|length)==0) | "    part\(.part) \(.name) :: \(.desc[0:60])"' "$FINAL" | head -20
  echo "[FATAL] 补齐 /tmp/zh/out_NN.json 后重跑 m5_render.sh"
  exit 1
fi
if [ "$n_newline" -gt 0 ]; then
  echo "[M5-WARN] $n_newline 条 zh 含换行，已强制折叠为空格"
  jq -c '.zh_final |= gsub("\n";" ")' "$FINAL" > "$FINAL.tmp" && mv "$FINAL.tmp" "$FINAL"
fi

# 4) 生成三部分 Markdown（按 name 排序，表格内 | 转义）
render_part() {  # render_part <part> <标题> <扫描目录说明>
  local part="$1" title="$2" root="$3" n
  n=$(jq -s --argjson p "$part" '[.[]|select(.part==$p)]|length' "$FINAL")
  echo "## $title"
  echo ""
  echo "扫描目录：\`$root\`"
  echo ""
  echo "共 **$n** 个 \`SKILL.md\`。"
  echo ""
  echo "| 技能 | 路径 | 说明 |"
  echo "|------|------|------|"
  jq -r -s --argjson p "$part" '
    [.[]|select(.part==$p)] | sort_by(.name) | .[] |
    "| `\(.name)` | `\(.rel)` | \(.zh_final | gsub("\\|";"\\\\|")) |"
  ' "$FINAL"
  echo ""
}

{
  echo "# 技能总览"
  echo ""
  echo "本文档汇总三个技能目录：\`~/.agents/skills/\`、\`agent-skills/skills/\` 与 \`agent-skills/self-skills/\`，根据各目录下实际存在的 \`SKILL.md\` 递归生成。技能名称优先读取 frontmatter \`name\`（缺失回退目录名）；说明为基于原始 \`description\` 提炼的中文摘要（≤500 字，简洁概括用途与触发场景）。"
  echo ""
  render_part 1 "第一部分：\`~/.agents/skills/\`" "$RUNTIME_SKILLS/（运行时技能目录）"
  render_part 2 "第二部分：\`agent-skills/skills/\`" "$KB_SKILLS/（外部 skill 副本库）"
  render_part 3 "第三部分：\`agent-skills/self-skills/\`（用户自写）" "$KB_SELF_SKILLS/（用户自写 skill 真源）"
} > "$DOC"

# 5) 快照重建（全量条目 abs→{mtime,name,zh}；磁盘已删条目自然移除）
jq -s 'map({key:.abs, value:{mtime:.mtime,name:.name,zh:.zh_final}}) | from_entries' "$FINAL" > "$SNAP"

# 6) 验证报告
p1=$(jq -s '[.[]|select(.part==1)]|length' "$FINAL")
p2=$(jq -s '[.[]|select(.part==2)]|length' "$FINAL")
p3=$(jq -s '[.[]|select(.part==3)]|length' "$FINAL")
n_cached=$(jq -s '[.[]|select(.cached==true)]|length' "$FINAL")
n_dirty=$((n_total - n_cached))
stats=$(jq -s '[.[]|.zh_final|length] | "min=\(min) max=\(max) mean=\((add/length)|round) median=\(sort[(length/2|floor)])"' "$FINAL")
echo "[M5-DONE] $DOC 已生成"
echo "[M5-STAT] 总数 ${n_total}（part1 $p1 / part2 $p2 / part3 ${p3}）缓存复用 $n_cached / 新翻译 $n_dirty / 超500字 $n_over / 长度 $stats"
echo "[M5-STAT] 快照已更新: ${SNAP}（不参与 git 提交，确认已在 .gitignore）"
