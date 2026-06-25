# ============================================================================
# 共用基础层：以下从 FROM 到“共用基础层结束”之间的内容，
# 在三个 Dockerfile（anima-trainer / caption_manager / wd-llm-caption-cli）中必须
# 保持【逐字节完全一致】。这样 BuildKit 会把这些层缓存下来并在三次构建间复用，
# 基础镜像也只会拉取/存储一份，从而最大化共享构建缓存。
# ============================================================================
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV TZ=Asia/Shanghai
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
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# ============================ 共用基础层结束 ============================

# ---- wd-llm-caption 专属部分 ----
WORKDIR /workspace

RUN pip install -U pip setuptools wheel

RUN git clone --branch v0.1.4-alpha --depth 1 https://github.com/fireicewolf/wd-llm-caption-cli.git /workspace/wd-llm-caption-cli
WORKDIR /workspace/wd-llm-caption-cli

# 安装 PyTorch（CUDA 12.4）
RUN pip install torch==2.5.0 torchvision --index-url https://download.pytorch.org/whl/cu124

# 安装项目依赖
RUN pip install -U -r requirements_wd.txt \
    && pip install -U -r requirements_onnx_cu12x.txt \
    && pip install -U -r requirements_llm.txt \
    && pip install -U -r requirements_huggingface.txt \
    && pip install -U -r requirements_modelscope.txt \
    && pip install -U -r requirements_gui.txt

# 修正上游未锁定的依赖版本：
# 1) requirements_gui.txt 写的是 gradio>=5.1.0，会装到 6.x，但项目代码只兼容 Gradio 5
#    （Textbox.show_copy_button 在 6.0 被移除）
# 2) modelscope 会把 huggingface_hub 升级到 1.x，但 transformers 4.45.2 要求 <1.0
# 3) Florence-2 的 modeling_florence2.py 远程动态加载时需要 einops，但项目 requirements 漏写
RUN pip install "gradio>=5.1.0,<6.0" "huggingface_hub<1.0" einops

# 开放 Gradio GUI 端口
EXPOSE 8282

# 默认启动 GUI，允许远程访问
CMD ["python", "gui.py", "--listen", "--port", "8282"]
