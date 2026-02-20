# Contributing

## Development setup

This project uses Python + JavaScript tooling:

- Python: managed with [`uv`](https://github.com/astral-sh/uv)
- Node: from `.nvmrc` (`v24`)
- pnpm: pinned to `10.30.1` via Corepack

```sh
corepack enable
corepack prepare pnpm@10.30.1 --activate
pnpm install --frozen-lockfile
uv sync --group dev --group test
```

## Local development

Run the example notebook:

```sh
uv run jupyter lab example.ipynb
```

To rebuild frontend assets while editing `js/`:

```sh
pnpm dev
```

## QA

Run the main local quality gate:

```sh
uv run ruff check .
uv run ruff format --check .
uv run ty check .
pnpm format:check
pnpm lint
pnpm typecheck
pnpm build
uv run pytest -q -m "not e2e"
```

Run browser e2e separately:

```sh
uv sync --all-groups
uv run playwright install chromium
uv run pytest -q -m e2e
```
