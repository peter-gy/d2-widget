from pathlib import Path

from d2_widget import Widget
from d2_widget import _widget as widget_module
from d2_widget._model import CompileOptions
from d2_widget._widget import DEFAULT_OPTIONS


def test_widget_uses_default_options_without_sharing_state() -> None:
    first = Widget("x -> y")
    second = Widget("a -> b")

    assert first.options == DEFAULT_OPTIONS
    assert second.options == DEFAULT_OPTIONS

    first.options["target"] = "layers.demo.*"
    assert second.options["target"] == "*"
    assert DEFAULT_OPTIONS["target"] == "*"


def test_widget_respects_empty_options_dict() -> None:
    options: CompileOptions = {}
    widget = Widget("x -> y", options)
    assert widget.options == {}


def test_widget_copies_explicit_options() -> None:
    options: CompileOptions = {"themeID": 200, "sketch": True}
    widget = Widget("x -> y", options)

    assert widget.options == options
    options["themeID"] = 0
    assert widget.options["themeID"] == 200


def test_widget_static_assets_exist() -> None:
    static_dir = Path(widget_module.__file__).resolve().parent / "static"
    assert (static_dir / "widget.js").is_file()
    assert (static_dir / "widget.css").is_file()
