#!/bin/bash
# 模块 5 阶段一：脚本提取 + 增量比对 + 分批（确定性工作，翻译交 sub agent）
# 用法: m5_extract.sh
# 产出:
#   $WORK_DIR/m5_records.jsonl   每条 {part,name,rel,desc,abs,mtime,cached,zh}
#   $WORK_DIR/m5_idmap.jsonl     dirty unique 集 {id,name,desc}（按 name+desc 去重）
#   /tmp/zh/in_NN.json           每批 ≤45 个 [{id,name,desc}]，sub agent 读入写 out_NN.json
# 快照: docs/.skills-overview-mtimes.json（mtime 未变且已有 zh → cached 复用，不送翻译）
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

SNAP="$KB_DOCS/.skills-overview-mtimes.json"
RECORDS="$WORK_DIR/m5_records.jsonl"
IDMAP="$WORK_DIR/m5_idmap.jsonl"
ZH_DIR="/tmp/zh"
: > "$RECORDS"; : > "$IDMAP"
rm -rf "$ZH_DIR"; mkdir -p "$ZH_DIR"
[ -f "$SNAP" ] || SNAP=""

# frontmatter 解析：name（缺失回退目录名由调用方处理）+ description（多行折叠单行）
parse_frontmatter() {
  awk '
    BEGIN{ infm=0; indesc=0; desc=""; name="" }
    NR==1 && /^---[[:space:]]*$/ { infm=1; next }
    infm && /^---[[:space:]]*$/ { exit }
    infm {
      if (indesc) {
        if ($0 ~ /^[[:space:]]+/) {
          line=$0; gsub(/^[[:space:]]+/,"",line); desc=desc " " line; next
        } else indesc=0
      }
      if ($0 ~ /^name:/) {
        v=$0; sub(/^name:[[:space:]]*/,"",v); gsub(/^["'"'"']|["'"'"']$/,"",v); name=v
      } else if ($0 ~ /^description:/) {
        v=$0; sub(/^description:[[:space:]]*/,"",v)
        if (v ~ /^[>|]-?$/) { indesc=1 }
        else { gsub(/^["'"'"']|["'"'"']$/,"",v); desc=v }
      }
    }
    END{
      gsub(/\t/," ",name); gsub(/\t/," ",desc)
      gsub(/[[:space:]]+/," ",desc); gsub(/^[[:space:]]+|[[:space:]]+$/,"",desc)
      print name "\t" desc
    }
  ' "$1"
}

scan_part() {  # scan_part <part号> <扫描根目录>
  local part="$1" root="$2" f rel dir name desc parsed mtime cached zh snap_e
  [ -d "$root" ] || { echo "[WARN] 扫描目录不存在: $root" >&2; return 0; }
  while IFS= read -r f; do
    dir=$(dirname "$f")
    rel="${dir#"$root"/}"; [ "$rel" = "$dir" ] && rel="."
    parsed=$(parse_frontmatter "$f")
    name=$(printf '%s' "$parsed" | cut -f1)
    desc=$(printf '%s' "$parsed" | cut -f2-)
    [ -n "$name" ] || name=$(basename "$dir")          # name 缺失回退目录名
    [ -n "$desc" ] || desc="（无描述）"                  # description 为空兜底
    mtime=$(stat -f %m "$f" 2>/dev/null || echo 0)
    cached=false; zh=""
    if [ -n "$SNAP" ]; then
      snap_e=$(jq -c --arg p "$f" '.[$p] // empty' "$SNAP" 2>/dev/null)
      if [ -n "$snap_e" ]; then
        local snap_mt snap_zh
        snap_mt=$(printf '%s' "$snap_e" | jq -r '.mtime // 0')
        snap_zh=$(printf '%s' "$snap_e" | jq -r '.zh // ""')
        if [ "$snap_mt" = "$mtime" ] && [ -n "$snap_zh" ]; then
          cached=true; zh="$snap_zh"
        fi
      fi
    fi
    jq -cn --argjson part "$part" --arg name "$name" --arg rel "$rel" \
      --arg desc "$desc" --arg abs "$f" --argjson mtime "$mtime" \
      --argjson cached "$cached" --arg zh "$zh" \
      '{part:$part,name:$name,rel:$rel,desc:$desc,abs:$abs,mtime:$mtime,cached:$cached,zh:$zh}' \
      >> "$RECORDS"
  done < <(find "$root" -name SKILL.md -type f 2>/dev/null | sort)
}

scan_part 1 "$RUNTIME_SKILLS"
scan_part 2 "$KB_SKILLS"
scan_part 3 "$KB_SELF_SKILLS"

# dirty unique 去重（name+desc）→ id 分配 → 分批 ≤45
jq -c 'select(.cached==false) | {name,desc}' "$RECORDS" | sort -u | jq -s '.' > "$WORK_DIR/m5_dirty_unique.json"
jq -c '. | to_entries[] | {id:(.key+1),name:.value.name,desc:.value.desc}' "$WORK_DIR/m5_dirty_unique.json" > "$IDMAP"

n_unique=$(wc -l < "$IDMAP" | tr -d ' ')
if [ "$n_unique" -eq 0 ]; then
  echo "[M5-EXTRACT] dirty 集为空，跳过翻译，直接运行 m5_render.sh 用缓存生成文档"
else
  # 分批：每批 ≤45
  batch=1
  jq -s '.' "$IDMAP" | jq -c '.[]' | awk -v dir="$ZH_DIR" '
    { lines[NR]=$0 }
    END {
      b=1; n=0; out=sprintf("%s/in_%02d.json", dir, b); printf "[" > out
      for (i=1;i<=NR;i++) {
        if (n>0) printf "," >> out
        printf "%s", lines[i] >> out
        n++
        if (n==45 && i<NR) { printf "]\n" >> out; b++; n=0; out=sprintf("%s/in_%02d.json", dir, b); printf "[" > out }
      }
      printf "]\n" >> out
      print b > (dir "/.nbatches")
    }'
  # 清理可能多出的空批文件（尾部 "[" 未闭合的情况不存在：最后一批总有内容）
  nb=$(cat "$ZH_DIR/.nbatches" 2>/dev/null || echo 1)
  # 校验每批为合法 JSON
  i=1
  while [ "$i" -le "$nb" ]; do
    bf=$(printf '%s/in_%02d.json' "$ZH_DIR" "$i")
    jq -e . "$bf" >/dev/null 2>&1 || { echo "[FATAL] 批次文件非法 JSON: $bf"; exit 1; }
    i=$((i+1))
  done
  echo "[M5-EXTRACT] dirty unique $n_unique 个 → $nb 批（每批 ≤45）→ $ZH_DIR/in_NN.json"
  echo "[M5-EXTRACT] 下一步：并行派 sub agent（每轮 5 个）读 in_NN.json 翻译写 out_NN.json（[{id,zh}]，单行中文 ≤500 字，id 一一对应），完成后运行 m5_render.sh"
fi

# 统计
total=$(wc -l < "$RECORDS" | tr -d ' ')
p1=$(jq -s '[.[]|select(.part==1)]|length' "$RECORDS")
p2=$(jq -s '[.[]|select(.part==2)]|length' "$RECORDS")
p3=$(jq -s '[.[]|select(.part==3)]|length' "$RECORDS")
n_cached=$(jq -s '[.[]|select(.cached==true)]|length' "$RECORDS")
n_nondes=$(grep -c '（无描述）' "$RECORDS" || true)
# 快照中有但磁盘已删除的条目数（render 时从快照移除）
n_deleted=0
if [ -n "$SNAP" ]; then
  n_deleted=$(jq -r 'keys[]' "$SNAP" 2>/dev/null | while IFS= read -r k; do [ -f "$k" ] || echo x; done | wc -l | tr -d ' ')
fi
echo "[M5-STAT] 总数 ${total}（第一部分 $p1 / 第二部分 $p2 / 第三部分 ${p3}）缓存命中 $n_cached / dirty unique $n_unique / 缺失描述 $n_nondes / 快照已删条目 $n_deleted"
