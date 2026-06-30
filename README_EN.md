# caption_manager

[![Release](https://github.com/handsome-Druid/caption_manager/actions/workflows/release.yml/badge.svg)](https://github.com/handsome-Druid/caption_manager/actions/workflows/release.yml)

[中文](README.md) | **English**

A tag (caption) cleaning and management tool for LoRA training datasets: automatically removes redundant / blacklisted / character tags, batch-adds prefix tags, and provides a web UI for visual operation.

Built with FastAPI; the frontend is a built-in static page listening on port `1357` by default.

---

## Workflow

`caption_manager` serves as the "tag cleaning" step between image tagging and LoRA training, forming a complete pipeline with two other services defined in `docker/docker-compose.yml`:

```
Raw images
   │
   ▼
wd-llm-caption  ── Auto-tagging (WD Tagger generates .wdcaption and writes to .txt;
                   LLM tag cleaning is not yet supported — do not generate .llmcaption)
   │
   ▼
caption_manager ── Clean tags: remove blacklisted / overlapping / character tags,
                   add prefix tags (this project)
   │
   ▼
anima-trainer   ── LoRA training on the cleaned dataset
```

All three services share the same `datasets/` directory and process the training set in sequence. Web UI ports:

- `wd-llm-caption`: `8282`
- `caption-manager`: `1357`
- `anima-trainer`: `13000`

For usage details of each upstream service, refer to their respective repositories: [wd-llm-caption-cli](https://github.com/fireicewolf/wd-llm-caption-cli) · [Anima-Standalone-Trainer](https://github.com/gazingstars123/Anima-Standalone-Trainer).

### Tag File Conventions

- Only `.txt` tag files that share the **same name** as an image are processed (e.g. `example.png` → `example.txt`). `.txt` files without a matching image are ignored.
- Tags are comma-separated and are written back with commas after processing.
- **LLM-generated natural-language tags are not yet supported for cleaning** — do not generate `.llmcaption` files during the tagging stage.

### Web UI Usage

Open `http://<host>:1357`, then:

1. **View & Remove Tags** — Enter a dataset sub-directory (relative to `datasets/`) to load all tags and their occurrence counts. Select tags and click to remove them in one step (`custom_remove`).
2. **Auto-Remove Configuration** (`auto_remove`):
   - Blacklisted tags are always removed (based on `filtering_tags/blacklist_tags.txt`).
   - `overlap`: removes overlapping / redundant tags that are covered by more specific tags.
   - `character_range`: intensity of character tag removal — `0` removes blacklist only; `1` also removes human-related character tags; `2` additionally removes beast-related tags such as cat ears and tails.
3. **Add Prefix Tags** (`add_prefix`) — Prepends specified tags to every tag file in order. Tags that already exist are moved to the front rather than duplicated.

### HTTP API

| Method | Path | Description |
| --- | --- | --- |
| GET  | `/v1/check_captions?folder=` | Read tags and counts in a directory |
| POST | `/v1/custom_remove` | Remove specified tags |
| POST | `/v1/auto_remove` | Auto-clean by configuration |
| POST | `/v1/add_prefix` | Add prefix tags |

API docs: `http://<host>:1357/docs`.

---

## Docker Deployment

`docker/docker-compose.yml` orchestrates `anima-trainer`, `caption-manager`, and `wd-llm-caption` together. Fixed-version images are used by default for easy pull, start, and rollback; you can rebuild individual services for local validation.

### 1. Start the Full Pipeline

```bash
docker compose up -d
```

To start only a specific service:

```bash
docker compose up -d caption-manager
```

### 2. Build a Single Image

To verify a Dockerfile locally, inspect build cache, or confirm an image has not been tampered with:

```bash
docker compose build caption-manager
docker compose build anima-trainer
docker compose build wd-llm-caption
```

Skip cache and force a full rebuild:

```bash
docker compose build --no-cache caption-manager
```

### 3. Run a Single Service

After building or pulling, start a specific service:

```bash
docker compose up -d caption-manager
```

`caption-manager` service details:

- Port: `1357:1357`
- Volumes:
   - `./datasets` → dataset directory
   - `./caption-manager/filtering_tags` → filter tag configuration directory

On first startup, the container automatically restores `filtering_tags` from the default files bundled in the image.

Version information for the `caption-manager` image is in [docker/caption-manager/NOTICE.md](docker/caption-manager/NOTICE.md).

---

## Local Run

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv run --no-dev caption-manager
```

View available options:

```bash
uv run --no-dev caption-manager --help
```

---

## Configuration

Configurable via CLI arguments or environment variables. You can copy `.env.example` to `.env`:

| Environment Variable | Default | Description |
| --- | --- | --- |
| `CAPTION_MANAGER_HOST` | `127.0.0.1` | Listen address |
| `CAPTION_MANAGER_PORT` | `1357` | Listen port |
| `CAPTION_MANAGER_BLACKLIST_TAGS_FILE` | `blacklist_tags.txt` | Blacklist tag file (inside `filtering_tags/`) |
| `CAPTION_MANAGER_OVERLAP_TAGS_FILE` | `overlap_tags.json` | Overlap tags file |
| `CAPTION_MANAGER_CHARACTER_TAGS_FILE` | `character_tags.json` | Character tags file |
| `CAPTION_MANAGER_DEBUG` | `false` | Debug mode (returns exception details to the frontend) |

All filter rule files are located in the [`filtering_tags/`](filtering_tags/) directory and can be customized as needed.

---

## Upstream Dependencies

Upstream projects and third-party filter tag data used by this project:

| Upstream Repository | Version | License |
| --- | --- | --- |
| [gazingstars123/Anima-Standalone-Trainer](https://github.com/gazingstars123/Anima-Standalone-Trainer) | `v2.2.0` | Apache-2.0 |
| [fireicewolf/wd-llm-caption-cli](https://github.com/fireicewolf/wd-llm-caption-cli) | `v0.1.4-alpha` | Apache-2.0 |
| [cyber-meow/anime_screenshot_pipeline/configs/tag_filtering](https://github.com/cyber-meow/anime_screenshot_pipeline/tree/c9e3fb804c3847d136c2124a68c7af4b17ef3219/configs/tag_filtering) | `c9e3fb804c3847d136c2124a68c7af4b17ef3219` | MIT |

Notes:

- Models pulled from ModelScope at runtime by `wd-llm-caption` have their own independent licenses, which must also be respected.
- Third-party attribution details are in [docker/anima-trainer/NOTICE.md](docker/anima-trainer/NOTICE.md), [docker/wd-llm-caption-cli/NOTICE.md](docker/wd-llm-caption-cli/NOTICE.md), and [filtering_tags/NOTICE.md](filtering_tags/NOTICE.md).

---

## License

This project's license is in [LICENSE](LICENSE).

License information for third-party filter tag data is in [filtering_tags/NOTICE.md](filtering_tags/NOTICE.md) and [filtering_tags/THIRD_PARTY_LICENSE](filtering_tags/THIRD_PARTY_LICENSE).
