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

# ---- caption_manager 专属部分 ----
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

ENV UV_PYTHON=3.13t
ENV PYTHON_GIL=0

RUN git clone --branch v0.4.6 https://github.com/handsome-Druid/caption_manager.git --depth 1
WORKDIR /caption_manager

RUN mkdir -p /caption_manager_defaults \
    && cp -r /caption_manager/filtering_tags /caption_manager_defaults/filtering_tags

RUN uv sync --no-dev

RUN cp /caption_manager/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 1357

RUN cp .env.example .env

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["uv", "run", "--no-dev", "caption-manager"]
