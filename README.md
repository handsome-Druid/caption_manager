# caption_manager

[![Release](https://github.com/handsome-Druid/caption_manager/actions/workflows/release.yml/badge.svg)](https://github.com/handsome-Druid/caption_manager/actions/workflows/release.yml)

用于 LoRA 训练数据集的标签（caption）清洗与管理工具：自动移除冗余 / 黑名单 / 角色标签，批量添加前缀标签，并提供 Web 界面进行可视化操作。

基于 FastAPI 构建，前端为内置静态页面，默认监听 `1357` 端口。

---

## 工作流

`caption_manager` 通常作为图像打标到 LoRA 训练之间的「标签清洗」环节，配合 `docker/docker-compose.yml` 中的另外两个服务组成完整流水线：

```
原始图片
   │
   ▼
wd-llm-caption  ── 自动打标（WD Tagger 生成 .wdcaption，写入 .txt；暂不支持清洗 LLM 标签，打标时请勿生成 .llmcaption）
   │
   ▼
caption_manager ── 清洗标签：移除黑名单 / 重叠 / 角色标签，添加前缀（本项目）
   │
   ▼
anima-trainer   ── 使用清洗后的数据集进行 LoRA 训练
```

三个服务共享同一个 `datasets/` 目录，依次对其中的标签文件进行处理。

### 标签文件约定

- 工具只处理与图片**同名**的 `.txt` 标签文件（例如 `example.png` 对应 `example.txt`），没有对应图片的 `.txt` 会被忽略。
- 标签以英文逗号分隔，处理后回写时同样以逗号分隔。
- `.wdcaption` 为打标阶段的中间产物，不参与清洗。
- **暂不支持清洗 LLM 生成的自然语言标签**，打标阶段请不要生成 `.llmcaption`。

### Web 界面操作步骤

打开 `http://<host>:1357` 后：

1. **查看与移除标签** — 输入数据集子目录（相对 `datasets/`），加载当前目录所有标签及出现次数；点选后可一键移除选中标签（`custom_remove`）。
2. **自动移除配置**（`auto_remove`）：
   - 移除黑名单标签（始终执行，基于 `filtering_tags/blacklist_tags.txt`）。
   - `overlap`：移除被更具体标签覆盖的重叠 / 冗余标签。
   - `character_range`：角色标签处理强度——`0` 仅移除黑名单；`1` 额外移除人类相关角色标签；`2` 在 `1` 基础上再移除猫耳、尾巴等兽化标签。
3. **添加前缀标签**（`add_prefix`）— 将指定标签按顺序置于每个标签文件的最前面；已存在的标签会被移动到头部，不会重复。

### HTTP 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET  | `/v1/check_captions?folder=` | 读取目录下标签及计数 |
| POST | `/v1/custom_remove` | 移除指定标签 |
| POST | `/v1/auto_remove` | 按配置自动清洗 |
| POST | `/v1/add_prefix` | 添加前缀标签 |

接口文档：`http://<host>:1357/docs`。

---

## Docker 部署

### 方式一：完整流水线（推荐）

`docker/docker-compose.yml` 一并编排 `anima-trainer`、`caption-manager`、`wd-llm-caption` 三个服务，共享 `datasets/` 目录。

```bash
cd docker
docker compose up -d caption-manager
```

如需启动完整流水线（需要 NVIDIA GPU 支持）：

```bash
docker compose up -d
```

`caption-manager` 服务说明：

- 端口：`1357:1357`
- 数据卷：
  - `./datasets` → 数据集目录
  - `./caption-manager/filtering_tags` → 过滤标签配置目录
- 环境变量：`CAPTION_MANAGER_HOST=0.0.0.0`（容器内对外监听）

容器首次启动时，若挂载的 `filtering_tags` 目录为空，`docker-entrypoint.sh` 会自动从镜像内置的默认文件恢复。

`caption-manager` 镜像在构建时从本仓库 `git clone` 拉取指定 tag 的源码，拉取版本见 [docker/caption-manager/NOTICE.md](docker/caption-manager/NOTICE.md)（该 tag 由发布工作流自动同步）。

### 方式二：单独构建镜像

```bash
docker build -t caption-manager:latest -f docker/caption-manager/Dockerfile .

docker run -d \
  -p 1357:1357 \
  -e CAPTION_MANAGER_HOST=0.0.0.0 \
  -v "$(pwd)/datasets:/caption_manager/datasets" \
  -v "$(pwd)/filtering_tags:/caption_manager/filtering_tags" \
  caption-manager:latest
```

---

## 本地运行

依赖 [uv](https://docs.astral.sh/uv/) 与 Python ≥ 3.13。

```bash
uv sync --no-dev
uv run caption-manager
```

常用参数（也可通过环境变量配置，见下）：

```bash
uv run caption-manager --host 0.0.0.0 --port 1357 --debug
```

查看版本：`uv run caption-manager --version`。

---

## 配置

支持通过命令行参数或环境变量配置，可复制 `.env.example` 为 `.env`：

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `CAPTION_MANAGER_HOST` | `127.0.0.1` | 监听地址 |
| `CAPTION_MANAGER_PORT` | `1357` | 监听端口 |
| `CAPTION_MANAGER_BLACKLIST_TAGS_FILE` | `blacklist_tags.txt` | 黑名单标签文件（位于 `filtering_tags/`） |
| `CAPTION_MANAGER_OVERLAP_TAGS_FILE` | `overlap_tags.json` | 重叠标签文件 |
| `CAPTION_MANAGER_CHARACTER_TAGS_FILE` | `character_tags.json` | 角色标签文件 |
| `CAPTION_MANAGER_DEBUG` | `false` | 调试模式（将异常详情返回前端） |

过滤规则文件均位于 [`filtering_tags/`](filtering_tags/) 目录，可按需自定义。

---

## 上游依赖仓库

完整流水线中的另外两个服务并不包含上游源码，其代码在镜像构建时由对应 `Dockerfile` 通过 `git clone` 从下列仓库拉取：

| 服务 | 上游仓库 | 版本 | 许可证 |
| --- | --- | --- | --- |
| anima-trainer | [gazingstars123/Anima-Standalone-Trainer](https://github.com/gazingstars123/Anima-Standalone-Trainer) | `v2.2.0` | Apache-2.0 |
| wd-llm-caption | [fireicewolf/wd-llm-caption-cli](https://github.com/fireicewolf/wd-llm-caption-cli) | `v0.1.4-alpha` | Apache-2.0 |

> **构建或使用上述两个 Docker 服务（及其镜像），即视为你已知悉并同意对应上游仓库的许可证条款**；其中 wd-llm-caption 运行时从 ModelScope 拉取的各模型另有独立许可证，亦需自行遵守。详见各目录下的 NOTICE：[docker/anima-trainer/NOTICE.md](docker/anima-trainer/NOTICE.md)、[docker/wd-llm-caption-cli/NOTICE.md](docker/wd-llm-caption-cli/NOTICE.md)。

---

## License

详见 [LICENSE](LICENSE)。第三方过滤标签数据的许可信息见 [filtering_tags/NOTICE.md](filtering_tags/NOTICE.md) 与 [filtering_tags/THIRD_PARTY_LICENSE](filtering_tags/THIRD_PARTY_LICENSE)。
