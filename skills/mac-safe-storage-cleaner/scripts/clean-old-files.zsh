#!/bin/zsh

THRESHOLD_GB=50
GENERAL_AGE_DAYS=30
IDEA_AGE_DAYS=3
WORKSPACE_AGE_DAYS=90
PRIVATE_TMP_AGE_DAYS=30
PRIVATE_VAR_TMP_AGE_DAYS=90

CACHE_DIR="$HOME/Library/Caches"
LOG_DIR="$HOME/Library/Logs"
IDEA_LOG_DIR="$HOME/Library/Logs/JetBrains"
DOWNLOAD_DIR="$HOME/Downloads"
DOCUMENTS_DIR="$HOME/Documents"
WORKSPACE_CHECKPOINTS_DIR="$HOME/.local/share/workspace-checkpoints"
WORKSPACE_CACHE_DIR="$HOME/.local/share/workspace-code-prd/cache"
ALLOWED_UNDER_PROTECTED_DIRS=(
  "$WORKSPACE_CHECKPOINTS_DIR"
  "$WORKSPACE_CACHE_DIR"
)
PROTECTED_DIRS=(
  "$HOME/aiot"
  "$HOME/.m2"
  "$HOME/.ssh"
  "$HOME/Library/Keychains"
  "$HOME/Library/Mail"
  "$HOME/Library/Messages"
  "$HOME/Library/Photos"
  "$HOME/Library/Application Support"
  "$HOME/Library/Containers"
  "$HOME/.local"
)
TEMP_DIRS=(
  "/private/tmp"
  "/private/var/tmp"
)

temp_age_days() {
  case "$1" in
    "/private/tmp")
      echo "$PRIVATE_TMP_AGE_DAYS"
      ;;
    "/private/var/tmp")
      echo "$PRIVATE_VAR_TMP_AGE_DAYS"
      ;;
    *)
      return 1
      ;;
  esac
}

preview_temp_files() {
  local dir="$1"
  local age_days

  age_days=$(temp_age_days "$dir") || return 1

  case "$dir" in
    "/private/tmp")
      # 参考 macOS periodic 的思路，只保留系统临时目录；名称里包含 workspace/ws 的普通文件不豁免。
      find "$dir" -mindepth 1 \
        \( -path "$dir/com.apple.launchd.*" -o -path "$dir/com.apple.launchd.*/*" \
        -o -path "$dir/TemporaryItems" -o -path "$dir/TemporaryItems/*" \) -prune \
        -o -type f -mtime +"$age_days" -print 2>/dev/null
      ;;
    "/private/var/tmp")
      # 这里只忽略系统保留临时目录；名称里包含 workspace/ws 的普通文件仍按规则清理。
      find "$dir" -mindepth 1 \
        \( -path "$dir/com.apple.launchd.*" -o -path "$dir/com.apple.launchd.*/*" \) -prune \
        -o -type f -mtime +"$age_days" -print 2>/dev/null
      ;;
  esac
}

delete_temp_files() {
  local dir="$1"
  local age_days

  age_days=$(temp_age_days "$dir") || return 1

  # 管道执行时 stdin 已 EOF，sudo 无法交互读密码。先检测 NOPASSWD 是否可用。
  local use_sudo=""
  if sudo -n true 2>/dev/null; then
    use_sudo="sudo"
  fi

  case "$dir" in
    "/private/tmp")
      $use_sudo find "$dir" -mindepth 1 \
        \( -path "$dir/com.apple.launchd.*" -o -path "$dir/com.apple.launchd.*/*" \
        -o -path "$dir/TemporaryItems" -o -path "$dir/TemporaryItems/*" \) -prune \
        -o -type f -mtime +"$age_days" -delete 2>/dev/null
      ;;
    "/private/var/tmp")
      $use_sudo find "$dir" -mindepth 1 \
        \( -path "$dir/com.apple.launchd.*" -o -path "$dir/com.apple.launchd.*/*" \) -prune \
        -o -type f -mtime +"$age_days" -delete 2>/dev/null
      ;;
  esac

  if [[ -z "$use_sudo" ]]; then
    echo "  [提示] $dir：未配置 NOPASSWD sudo，仅清理了当前用户可访问的文件。root 拥有的旧文件需手动执行 sudo 清理。"
  fi
}

is_allowed_under_protected() {
  local target="$1"
  local allowed_dir

  for allowed_dir in "${ALLOWED_UNDER_PROTECTED_DIRS[@]}"; do
    if [[ "$target" == "$allowed_dir" || "$target" == "$allowed_dir"/* ]]; then
      return 0
    fi
  done

  return 1
}

SAFETY_TARGETS=(
  "$CACHE_DIR"
  "$LOG_DIR"
  "$DOWNLOAD_DIR"
  "$DOCUMENTS_DIR"
  "$WORKSPACE_CHECKPOINTS_DIR"
  "$WORKSPACE_CACHE_DIR"
)

for target_dir in "${SAFETY_TARGETS[@]}"; do
  for protected_dir in "${PROTECTED_DIRS[@]}"; do
    if [[ "$target_dir" == "$protected_dir" || "$target_dir" == "$protected_dir"/* ]]; then
      if ! is_allowed_under_protected "$target_dir"; then
        echo "安全检查失败：清理目录命中了受保护路径：$target_dir"
        exit 1
      fi
    fi
  done
done

total_kb=0

echo "正在统计缓存、日志和临时文件占用..."

for dir in "$CACHE_DIR" "$LOG_DIR" "$DOWNLOAD_DIR" "$DOCUMENTS_DIR" \
  "$WORKSPACE_CHECKPOINTS_DIR" "$WORKSPACE_CACHE_DIR" "${TEMP_DIRS[@]}"; do
  if [[ -d "$dir" ]]; then
    size_kb=$(du -sk "$dir" 2>/dev/null | cut -f1)
    total_kb=$((total_kb + size_kb))
  fi
done

total_gb=$((total_kb / 1024 / 1024))

echo
echo "各目录占用："
for dir in "$CACHE_DIR" "$LOG_DIR" "$DOWNLOAD_DIR" "$DOCUMENTS_DIR" \
  "$WORKSPACE_CHECKPOINTS_DIR" "$WORKSPACE_CACHE_DIR" "${TEMP_DIRS[@]}"; do
  if [[ -d "$dir" ]]; then
    du -sh "$dir" 2>/dev/null
  fi
done

echo
echo "IDEA/JetBrains 日志占用："
du -sh "$IDEA_LOG_DIR" 2>/dev/null || echo "未找到"

echo
echo "工作区历史检查点和缓存占用："
du -sh "$WORKSPACE_CHECKPOINTS_DIR" "$WORKSPACE_CACHE_DIR" 2>/dev/null

echo
echo "文稿目录只统计，不自动删除："
find "$DOCUMENTS_DIR" -type f -mtime +90 -size +1G -print 2>/dev/null

echo
echo "受保护目录："
printf '  %s\n' "${PROTECTED_DIRS[@]}"

echo
echo "受保护目录下允许按 ${WORKSPACE_AGE_DAYS} 天清理的 Workspace 路径："
printf '  %s\n' "${ALLOWED_UNDER_PROTECTED_DIRS[@]}"

echo
echo "待处理目录总占用约 ${total_gb} GB"
echo "清理阈值：${THRESHOLD_GB} GB"

if (( total_gb < THRESHOLD_GB )); then
  echo "未超过 ${THRESHOLD_GB} GB，不执行清理。"
  exit 0
fi

echo
echo "将预览待删除文件..."

echo
echo "[普通缓存：${GENERAL_AGE_DAYS} 天以前]"
find "$CACHE_DIR" -type f -mtime +"$GENERAL_AGE_DAYS" -print 2>/dev/null

echo
echo "[普通日志：${GENERAL_AGE_DAYS} 天以前，不包含 IDEA 日志]"
find "$LOG_DIR" \
  -path "$IDEA_LOG_DIR" -prune \
  -o -type f -mtime +"$GENERAL_AGE_DAYS" -print 2>/dev/null

echo
echo "[IDEA/JetBrains 日志：${IDEA_AGE_DAYS} 天以前]"
find "$IDEA_LOG_DIR" -type f -mtime +"$IDEA_AGE_DAYS" -print 2>/dev/null

for dir in "${TEMP_DIRS[@]}"; do
  echo
  age_days=$(temp_age_days "$dir") || continue
  echo "[$dir：${age_days} 天以前，忽略系统保留临时目录]"
  preview_temp_files "$dir"
done

echo
echo "[下载目录中的安装包和压缩包：${GENERAL_AGE_DAYS} 天以前]"
find "$DOWNLOAD_DIR" -type f -mtime +"$GENERAL_AGE_DAYS" \
  \( -iname "*.dmg" -o -iname "*.pkg" -o -iname "*.zip" \
  -o -iname "*.tar" -o -iname "*.tar.gz" -o -iname "*.tgz" \
  -o -iname "*.7z" \) -print 2>/dev/null

echo
echo "[工作区检查点：${WORKSPACE_AGE_DAYS} 天以前]"
if pgrep -x ws >/dev/null 2>&1; then
  echo "ws 当前正在运行，跳过工作区检查点清理。"
else
  find "$WORKSPACE_CHECKPOINTS_DIR/shadowGit" \
    -mindepth 1 -maxdepth 1 -type d \
    -mtime +"$WORKSPACE_AGE_DAYS" -print 2>/dev/null
fi

echo
echo "[工作区缓存：${WORKSPACE_AGE_DAYS} 天以前]"
if pgrep -x ws >/dev/null 2>&1; then
  echo "ws 当前正在运行，跳过工作区缓存清理。"
else
  find "$WORKSPACE_CACHE_DIR" \
    -type f -mtime +"$WORKSPACE_AGE_DAYS" -print 2>/dev/null
fi

echo
read "answer?确认删除以上旧文件？输入 DELETE 继续："

if [[ "$answer" != "DELETE" ]]; then
  echo "已取消清理。"
  exit 0
fi

echo
echo "开始清理..."

find "$CACHE_DIR" -type f -mtime +"$GENERAL_AGE_DAYS" -delete 2>/dev/null

find "$LOG_DIR" \
  -path "$IDEA_LOG_DIR" -prune \
  -o -type f -mtime +"$GENERAL_AGE_DAYS" -delete 2>/dev/null

find "$IDEA_LOG_DIR" -type f -mtime +"$IDEA_AGE_DAYS" -delete 2>/dev/null

for dir in "${TEMP_DIRS[@]}"; do
  delete_temp_files "$dir"
done

find "$DOWNLOAD_DIR" -type f -mtime +"$GENERAL_AGE_DAYS" \
  \( -iname "*.dmg" -o -iname "*.pkg" -o -iname "*.zip" \
  -o -iname "*.tar" -o -iname "*.tar.gz" -o -iname "*.tgz" \
  -o -iname "*.7z" \) -delete 2>/dev/null

if pgrep -x ws >/dev/null 2>&1; then
  echo "ws 当前正在运行，未清理工作区检查点。"
else
  find "$WORKSPACE_CHECKPOINTS_DIR/shadowGit" \
    -mindepth 1 -maxdepth 1 -type d \
    -mtime +"$WORKSPACE_AGE_DAYS" -exec rm -rf {} + 2>/dev/null
fi

if pgrep -x ws >/dev/null 2>&1; then
  echo "ws 当前正在运行，未清理工作区缓存。"
else
  find "$WORKSPACE_CACHE_DIR" \
    -type f -mtime +"$WORKSPACE_AGE_DAYS" -delete 2>/dev/null
fi

echo
echo "清理完成。"
