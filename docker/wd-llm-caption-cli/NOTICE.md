# 第三方上游来源说明

本目录仅包含本项目编写的 `Dockerfile`，**不包含**任何上游源码。上游代码在镜像构建时由 `Dockerfile` 通过 `git clone` 从下列仓库拉取，本仓库不对其进行再分发。

## 上游项目

- 项目：[fireicewolf/wd-llm-caption-cli](https://github.com/fireicewolf/wd-llm-caption-cli)
- 构建版本：`v0.1.4-alpha`
- 许可证：Apache License 2.0（许可证全文见上游仓库 `LICENSE`）

## 说明

- 该工具在运行时会按需下载 WD Tagger、Joy-Caption、Llama 3.2 Vision、Qwen2-VL、MiniCPM-V、Florence-2 等模型；本镜像已配置为从 ModelScope 拉取模型，无需 Hugging Face 的 gated 访问授权或 `HF_TOKEN`。这些模型各自有独立的许可证，请自行遵守对应模型的使用条款。
- 构建出的**镜像**中会打包上述上游代码及其依赖；如分发镜像，请遵守上游 Apache-2.0 许可证条款（包括保留版权声明与 NOTICE）。
- 构建与使用本目录的 `Dockerfile`，即视为你已知悉并同意上述上游项目及其所用模型的许可证条款。
- 如需追踪上游更新，建议同步时记录所采用的上游 commit hash 以便审计。
