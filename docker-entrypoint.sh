#!/bin/sh
set -e

# 若 filtering_tags 挂载目录为空，从镜像备份中恢复默认文件
if [ -z "$(ls -A /caption_manager/filtering_tags 2>/dev/null)" ]; then
    echo "filtering_tags is empty, copying defaults..."
    cp -r /caption_manager_defaults/filtering_tags/. /caption_manager/filtering_tags/
fi

exec "$@"
