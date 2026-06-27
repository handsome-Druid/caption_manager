# 镜像构建来源说明

本目录仅包含本项目编写的 `Dockerfile`，**不包含**任何源码。`caption_manager` 源码在镜像构建时由 `Dockerfile` 通过 `git clone` 从本项目仓库拉取。

## 拉取版本

- 仓库：[handsome-Druid/caption_manager](https://github.com/handsome-Druid/caption_manager)
- 构建版本：`v0.4.4`
- 许可证：BSD 3-Clause（见仓库根目录 [`LICENSE`](../../LICENSE)）

## 说明

- 构建出的**镜像**中会打包本项目代码及其依赖；如分发镜像，请遵守本项目 BSD 3-Clause 许可证条款。
- 构建与使用本目录的 `Dockerfile`，即视为你已知悉并同意本项目的许可证条款。
