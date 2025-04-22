[![PyPI](https://img.shields.io/pypi/v/d2-widget.svg)](https://pypi.org/project/d2-widget/)

# D2 Widget <img src="./assets/logo.png" align="right" alt="d2-widget logo" width="150" style="filter: drop-shadow(3px 3px 3px rgba(0,0,0,0.3));"/>

> Bring the power of [D2](https://d2lang.com/) to Python notebooks.

**d2-widget** is an [AnyWidget](https://github.com/manzt/anywidget) for displaying declarative diagrams written in [D2](https://d2lang.com/).

## Installation

```sh
pip install d2-widget
```

or with [uv](https://github.com/astral-sh/uv):

```sh
uv add d2-widget
```

## Usage

The following examples demonstrate how to use Widget with increasing complexity.

### Basic Usage

The simplest way to use Widget is to pass a D2 diagram as a string to the constructor.

```python
from d2_widget import Widget

Widget("x -> y")
```

<img src="./assets/examples/simple.svg" alt="simple example" width="400"/>

### Inline Configuration

You can add direction and layout settings directly in the D2 markup.

```python
from d2_widget import Widget

Widget("""
direction: right
x -> y
""")
```

<img src="./assets/examples/simple-inline-config.svg" alt="simple example with inline configuration" width="400"/>

### Compile Options

You can specify compile options using the second argument to the constructor.
You can read about the semantics of the options in the [D2 documentation](https://www.npmjs.com/package/@terrastruct/d2#compileoptions).

```python
from d2_widget import Widget

Widget("""
direction: right
x -> y
""",
  {
      "themeID": 200,  # ID of the "Dark mauve" theme
      "pad": 0,        # Disable padding
      "sketch": True,  # Enable sketch mode
  },
)
```

<img src="./assets/examples/compile-options.svg" alt="example with compile options" width="400"/>

### Accessing the SVG

You can access the generated SVG using the `svg` attribute.

```python
from d2_widget import Widget

w = Widget("x -> y")
w.svg
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
