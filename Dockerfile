FROM ubuntu:22.04
ENV TZ=Asia/Shanghai
RUN sed -i -E 's/http:\/\/(archive|security).ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt -y install libcurl4 && DEBIAN_FRONTEND="noninteractive" apt -y install tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y --no-install-recommends git curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN git clone https://github.com/handsome-Druid/caption_manager.git --depth 1
WORKDIR /caption_manager

RUN cp -r /caption_manager/filtering_tags /caption_manager_defaults/filtering_tags

RUN uv sync --no-dev

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 1357

RUN cp .env.example .env

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["uv", "run", "--no-dev", "caption-manager"]
