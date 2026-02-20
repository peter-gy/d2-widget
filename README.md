[![PyPI](https://img.shields.io/pypi/v/d2-widget.svg)](https://pypi.org/project/d2-widget/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/peter-gy/d2-widget/blob/main/LICENSE)

# D2 Widget <img src="https://raw.githubusercontent.com/peter-gy/d2-widget/refs/heads/main/assets/logo.png" align="right" alt="d2-widget logo" width="150" style="filter: drop-shadow(3px 3px 3px rgba(0,0,0,0.3));"/>

> Bring the power of [D2](https://d2lang.com/) to Python notebooks.

**d2-widget** is an [AnyWidget](https://github.com/manzt/anywidget) for displaying declarative diagrams written in [D2](https://d2lang.com/).

- 🎨 **D2 Diagram Rendering**: Create and display interactive D2 diagrams directly in Python notebooks
- ⚙️ **Configurability**: Support for all D2 compilation options including themes, layouts, and rendering configurations
- 📤 **SVG Export**: Programmatically access the SVG representation for use in other documents
- ✨ **Jupyter Cell Magic**: Use the convenient `%%d2` cell magic for quick diagram creation
- 🧩 **Notebook Compatibility**: Works in Jupyter, Google Colab, Marimo, and other [AnyWidget](https://github.com/manzt/anywidget)-enabled Python notebook environments
- 🎬 **Animation Support**: Create animated diagrams with D2's native animation capabilities

## Playground

Visit the interactive [playground](https://d2-widget.peter.gy) to try out what `d2-widget` can do.

<img src="https://raw.githubusercontent.com/peter-gy/d2-widget/refs/heads/main/assets/examples/playground.gif" alt="playground" width="100%"/>

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

<img src="https://raw.githubusercontent.com/peter-gy/d2-widget/refs/heads/main/assets/examples/simple.svg" alt="simple example" width="400"/>

### Inline Configuration

You can add direction and layout settings directly in the D2 markup.

```python
from d2_widget import Widget

Widget("""
direction: right
x -> y
""")
```

<img src="https://raw.githubusercontent.com/peter-gy/d2-widget/refs/heads/main/assets/examples/simple-inline-config.svg" alt="simple example with inline configuration" width="400"/>

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

<img src="https://raw.githubusercontent.com/peter-gy/d2-widget/refs/heads/main/assets/examples/compile-options.svg" alt="example with compile options" width="400"/>

### Accessing the SVG

You can access the generated SVG using the `svg` attribute.

```python
from d2_widget import Widget

w = Widget("x -> y")
w.svg
```

### `%%d2` Cell Magic

You can use the `%%d2` cell magic to display a D2 diagram in a Jupyter notebook.

First, you need to load the extension:

```python
%load_ext d2_widget
```

Then, you can use the `%%d2` cell magic to display a D2 diagram.
You can pass compile options to the cell magic using keyword arguments.

```python
%%d2 sketch=True themeID=200
direction: right
x -> y
y -> z { style.animated: true }
z -> x
```

<img src="https://raw.githubusercontent.com/peter-gy/d2-widget/refs/heads/main/assets/examples/cell-magic.gif" alt="example with cell magic" width="100%"/>

## Contributing

Contributor setup, dev workflow, and QA commands are in [`CONTRIBUTING.md`](CONTRIBUTING.md).
