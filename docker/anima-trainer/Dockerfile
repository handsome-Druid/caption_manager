# ============================================================================
# 共用基础层：以下从 FROM 到“共用基础层结束”之间的内容，
# 在三个 Dockerfile（anima-trainer / caption_manager / wd-llm-caption-cli）中必须
# 保持【逐字节完全一致】。这样 BuildKit 会把这些层缓存下来并在三次构建间复用，
# 基础镜像也只会拉取/存储一份，从而最大化共享构建缓存。
# ============================================================================
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i -E 's/http:\/\/(archive|security).ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    sudo \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    libcurl4 \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# ============================ 共用基础层结束 ============================

# ---- anima-trainer 专属部分 ----

WORKDIR /anima-trainer

RUN git clone --branch v2.2.0 --depth 1 https://github.com/gazingstars123/Anima-Standalone-Trainer.git .

RUN chmod +x setup_env.sh && ./setup_env.sh

# 将 training-ui 期望的配置文件位置软链到挂载卷目录 /anima-trainer/config，
# 使配置持久化在宿主机，且镜像内不残留实际配置（构建期此链接为悬空，运行期由卷+entrypoint 填充）。
RUN ln -sfn /anima-trainer/config/global_config.toml /anima-trainer/training-ui/global_config.toml

# 入口脚本（烘焙进镜像）：首次启动且挂载卷为空时用模板初始化配置，
# 然后激活 venv 并执行 CMD。把初始化逻辑从 compose 内联 shell 移到这里。
RUN printf '%s\n' \
    '#!/bin/bash' \
    'set -e' \
    'mkdir -p /anima-trainer/config' \
    'if [ ! -f /anima-trainer/config/global_config.toml ]; then' \
    '    cp /anima-trainer/training-ui/global_config.template.toml /anima-trainer/config/global_config.toml' \
    'fi' \
    'source /anima-trainer/venv/bin/activate' \
    'exec "$@"' \
    > /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 3000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["bash", "./training-ui/start_linux.sh"]
