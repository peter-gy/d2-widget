# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "d2-widget",
#     "httpx==0.28.1",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full", app_title="D2 Playground")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # D2 Playground

        Dive into D2 with this interactive playground — create diagrams from scratch or explore curated examples.

        > Inspired by [play.d2lang.com](https://play.d2lang.com/), powered by [d2-widget](https://github.com/peter-gy/d2-widget) and [marimo](https://marimo.io/).
        >
        > Snippets curated from [terrastruct/d2-docs](https://github.com/terrastruct/d2-docs).
        """
    )
    return


@app.cell(hide_code=True)
def _(
    download_d2,
    download_svg,
    editor,
    mo,
    padding,
    scale,
    show_editor,
    sketch,
    theme,
    widget,
    with_label,
):
    mo.vstack(
        [
            mo.hstack(
                [
                    with_label(show_editor, "👀 Show Editor"),
                    with_label(theme, "🎨 Theme"),
                    with_label(sketch, "✏️ Sketch"),
                    with_label(padding, "↕️ Padding"),
                    with_label(scale, "🔍 Scale"),
                    mo.vstack([download_svg, download_d2]),
                ]
            ),
            mo.md("----"),
            mo.hstack(
                [
                    *([editor] if show_editor.value else []),
                    widget,
                ],
                widths="equal",
            ),
        ],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""---""")
    return


@app.cell(hide_code=True)
def _(snippets):
    snippets
    return


@app.cell(hide_code=True)
def _(get_script, mo, set_script):
    editor = mo.ui.code_editor(
        value=get_script(),
        min_height=400,
        max_height=800,
        show_copy_button=True,
        on_change=set_script,
        debounce=250,
    )
    return (editor,)


@app.cell(hide_code=True)
def _(d2_widget, mo):
    widget = mo.ui.anywidget(d2_widget.Widget(""))
    return (widget,)


@app.cell(hide_code=True)
def _(get_script, padding, scale, sketch, theme, theme_id, widget):
    widget.diagram = get_script()
    widget.options = {
        "target": "*",
        "sketch": sketch.value,
        "themeID": theme_id(theme.value),
        "pad": padding.value,
        "scale": scale.value,
        "animateInterval": 2000,
        "center": True,
    }
    return


@app.cell(hide_code=True)
def _(get_should_show_editor, mo, set_should_show_editor):
    show_editor = mo.ui.switch(
        get_should_show_editor(), on_change=set_should_show_editor
    )
    return (show_editor,)


@app.cell(hide_code=True)
def _(mo, theme_config):
    sketch = mo.ui.switch(False)

    theme = mo.ui.dropdown(
        options=[cfg["name"] for cfg in theme_config],
        value=theme_config[0]["name"],
        allow_select_none=False,
    )

    padding = mo.ui.slider(
        start=0,
        stop=150,
        step=10,
        value=50,
        debounce=True,
        show_value=True,
    )

    scale = mo.ui.slider(
        start=0,
        stop=1.0,
        step=0.05,
        value=1.0,
        debounce=True,
        show_value=True,
    )
    return padding, scale, sketch, theme


@app.cell(hide_code=True)
def _(mo, widget):
    download_svg = mo.download(
        data=widget.svg.encode("utf-8"),
        filename="diagram.svg",
        mimetype="image/svg+xml",
        label="Download SVG",
    )

    download_d2 = mo.download(
        data=widget.diagram.encode("utf-8"),
        filename="diagram.d2",
        mimetype="text/plain",
        label="Download D2",
    )
    return download_d2, download_svg


@app.cell(hide_code=True)
def _():
    theme_config = [
        {"id": 0, "name": "Default"},
        {"id": 1, "name": "Neutral gray"},
        {"id": 3, "name": "Flagship Terrastruct"},
        {"id": 4, "name": "Cool classics"},
        {"id": 5, "name": "Mixed berry blue"},
        {"id": 6, "name": "Grape soda"},
        {"id": 7, "name": "Aubergine"},
        {"id": 8, "name": "Colorblind clear"},
        {"id": 100, "name": "Vanilla nitro cola"},
        {"id": 101, "name": "Orange creamsicle"},
        {"id": 102, "name": "Shirley temple"},
        {"id": 103, "name": "Earth tones"},
        {"id": 104, "name": "Everglade green"},
        {"id": 105, "name": "Buttered toast"},
        {"id": 200, "name": "Dark mauve"},
        {"id": 300, "name": "Terminal"},
        {"id": 301, "name": "Terminal grayscale"},
    ]

    def theme_id(name: str) -> int:
        for cfg in theme_config:
            if cfg["name"] == name:
                return cfg["id"]

        raise ValueError(f"Unknown theme name: {name}")

    return theme_config, theme_id


@app.cell(hide_code=True)
def _(mo):
    def with_label(widget, label: str):
        return mo.vstack([mo.md(label), widget])

    return (with_label,)


@app.cell(hide_code=True)
def _(find_script, mo, set_script, set_should_show_editor, snippets_data):
    def on_snippet_selected(value: list[dict]):
        selection: dict = value[0]
        script = find_script(selection["Name"])
        set_script(script)
        set_should_show_editor(False)

    snippets = mo.ui.table(
        data=snippets_data,
        page_size=10,
        selection="single",
        on_change=on_snippet_selected,
    )
    return (snippets,)


@app.cell(hide_code=True)
def _(httpx):
    SNIPPETS_URL = "https://minio.peter.gy/static/drop/d2-snippets.json"
    snippets_data_full = httpx.get(SNIPPETS_URL).json()
    return (snippets_data_full,)


@app.cell(hide_code=True)
def _(snippets_data_full):
    snippets_data = [
        {
            "Category": s["category"],
            "Name": s["name"],
        }
        for s in snippets_data_full
    ]

    def find_script(name: str) -> str:
        for s in snippets_data_full:
            if s["name"] == name:
                return s["script"]

        raise ValueError(f'No script found for snippet "{name}"')

    return find_script, snippets_data


@app.cell(hide_code=True)
def _(INITIAL_SCRIPT, mo):
    get_script, set_script = mo.state(INITIAL_SCRIPT, allow_self_loops=False)
    get_should_show_editor, set_should_show_editor = mo.state(
        True, allow_self_loops=False
    )
    return (
        get_script,
        get_should_show_editor,
        set_script,
        set_should_show_editor,
    )


@app.cell(hide_code=True)
def _():
    INITIAL_SCRIPT = """direction: right

    nbenv: "Python Notebook Environment" {
      shape: image
      icon: https://minio.peter.gy/static/drop/notebook-envs.svg
    }

    d2widget: "d2-widget" {
      icon: https://minio.peter.gy/static/drop/d2-widget-logo.png
      d2: "D2" {
        shape: image
        icon: https://d2lang.com/img/d2_graphic.svg
      }

      anywidget {
        shape: image
        icon: https://anywidget.dev/favicon.svg
      }
    }

    d2widget.anywidget -> d2widget.d2 -> d2widget.anywidget {style.animated: true}

    nbenv -> d2widget {style.animated: true}
    """
    return (INITIAL_SCRIPT,)


@app.cell(hide_code=True)
def _():
    import httpx
    import marimo as mo

    import d2_widget

    return d2_widget, httpx, mo


if __name__ == "__main__":
    app.run()
