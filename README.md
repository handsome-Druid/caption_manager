# caption_manager

[![Release](https://github.com/handsome-Druid/caption_manager/actions/workflows/release.yml/badge.svg)](https://github.com/handsome-Druid/caption_manager/actions/workflows/release.yml)

用于 LoRA 训练数据集的标签（caption）清洗与管理工具：自动移除冗余 / 黑名单 / 角色标签，批量添加前缀标签，并提供 Web 界面进行可视化操作。

基于 FastAPI 构建，前端为内置静态页面，默认监听 `1357` 端口。

---

## 工作流

`caption_manager` 作为图像打标到 LoRA 训练之间的「标签清洗」环节，配合 `docker/docker-compose.yml` 中的另外两个服务组成完整流水线：

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
- **暂不支持清洗 LLM 生成的自然语言标签**，打标阶段请不要使用`llm`生成 `.llmcaption`。

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

`docker/docker-compose.yml` 一并编排 `anima-trainer`、`caption-manager`、`wd-llm-caption` 三个服务。默认使用固定版本镜像，便于按版本拉取、启动和回退；本地校验时，可直接重新构建对应服务。

### 1. 启动完整流水线

启动完整流水线：

```bash
docker compose up -d
```

如果只想启动某个服务，也可以指定服务名：

```bash
docker compose up -d caption-manager
```

### 2. 单独构建某个镜像

本地验证 Dockerfile、检查构建缓存或确认镜像未被篡改时，可只构建某个服务：

```bash
docker compose build caption-manager
docker compose build anima-trainer
docker compose build wd-llm-caption
```

跳过缓存、强制完整重建：

```bash
docker compose build --no-cache caption-manager
```

### 3. 单独运行某个服务

构建或拉取完成后，可以单独启动某个服务：

```bash
docker compose up -d caption-manager
```

`caption-manager` 服务说明：

- 端口：`1357:1357`
- 数据卷：
   - `./datasets` → 数据集目录
   - `./caption-manager/filtering_tags` → 过滤标签配置目录

容器首次启动时，会自动从镜像内置的默认文件恢复`filtering_tags`。

`caption-manager` 镜像对应的版本信息见 [docker/caption-manager/NOTICE.md](docker/caption-manager/NOTICE.md)。

---

## 本地运行

依赖 [uv](https://docs.astral.sh/uv/)。

```bash
uv run --no-dev caption-manager
```

查看参数：

```bash
uv run --no-dev caption-manager --help
```

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

本项目使用的上游项目及第三方过滤标签数据来源如下，便于确认镜像和仓库所包含的第三方来源：

| 上游仓库 | 版本 | 许可证 |
| --- | --- | --- |
| [gazingstars123/Anima-Standalone-Trainer](https://github.com/gazingstars123/Anima-Standalone-Trainer) | `v2.2.0` | Apache-2.0 |
| [fireicewolf/wd-llm-caption-cli](https://github.com/fireicewolf/wd-llm-caption-cli) | `v0.1.4-alpha` | Apache-2.0 |
| [cyber-meow/anime_screenshot_pipeline/configs/tag_filtering](https://github.com/cyber-meow/anime_screenshot_pipeline/tree/c9e3fb804c3847d136c2124a68c7af4b17ef3219/configs/tag_filtering) | `c9e3fb804c3847d136c2124a68c7af4b17ef3219` | MIT |

补充说明：

- `wd-llm-caption` 运行时从 ModelScope 拉取的各模型另有独立许可证，亦需自行遵守。
- 第三方来源说明见 [docker/anima-trainer/NOTICE.md](docker/anima-trainer/NOTICE.md)、[docker/wd-llm-caption-cli/NOTICE.md](docker/wd-llm-caption-cli/NOTICE.md) 与 [filtering_tags/NOTICE.md](filtering_tags/NOTICE.md)。

---

## License

本项目许可证见 [LICENSE](LICENSE)。

第三方过滤标签数据的许可信息见 [filtering_tags/NOTICE.md](filtering_tags/NOTICE.md) 与 [filtering_tags/THIRD_PARTY_LICENSE](filtering_tags/THIRD_PARTY_LICENSE)。
