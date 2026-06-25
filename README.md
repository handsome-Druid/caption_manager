# caption_manager

用于自动清洗和添加lora训练的角色标签

## Docker 部署

构建镜像：

```bash
docker build -t caption-manager:latest .
```

启动服务（`dataset/` 和 `filtering_tags/` 会挂载到容器中）：

```bash
docker compose up -d
```

服务默认监听 `1357` 端口。
