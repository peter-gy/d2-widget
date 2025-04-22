# D2 Widget <img src="./assets/logo.png" align="right" alt="d2-widget logo" width="150" style="filter: drop-shadow(3px 3px 3px rgba(0,0,0,0.3));"/>

> Bring the power of [D2](https://d2lang.com/) to Python notebooks.

**d2-widget** is an [anywidget](https://github.com/manzt/anywidget) for displaying declarative diagrams written in [D2](https://d2lang.com/).

## Installation

```sh
pip install d2-widget
```

or with [uv](https://github.com/astral-sh/uv):

```sh
uv add d2-widget
```

## Development

We recommend using [uv](https://github.com/astral-sh/uv) for development.
It will automatically manage virtual environments and dependencies for you.

```sh
uv run jupyter lab example.ipynb
```

Alternatively, create and manage your own virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
jupyter lab example.ipynb
```

The widget front-end code bundles it's JavaScript dependencies. After setting up Python,
make sure to install these dependencies locally:

```sh
pnpm install
```

While developing, you can run the following in a separate terminal to automatically
rebuild JavaScript as you make changes:

```sh
pnpm dev
```

Open `example.ipynb` in JupyterLab, VS Code, or your favorite editor
to start developing. Changes made in `js/` will be reflected
in the notebook.
