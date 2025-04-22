from d2_widget._version import __version__
from d2_widget._widget import Widget

__all__ = ["Widget", "__version__"]


def load_ipython_extension(ipython) -> None:  # type: ignore[no-untyped-def]
    """Extend IPython with interactive D2 widget display when using the `%d2` magic command."""
    from IPython.display import display
    from IPython.core.magic import register_cell_magic
    import json

    @register_cell_magic
    def d2(line, cell):
        options = {}
        if line.strip():
            try:
                # Try parsing as JSON
                options = json.loads(line)
            except json.JSONDecodeError:
                # Parse as key=value pairs
                for pair in line.split():
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        # Try to convert value to appropriate type
                        if value.isdigit():
                            value = int(value)
                        elif value.lower() in ("true", "false"):
                            value = value.lower() == "true"
                        options[key] = value

        display(Widget(cell, options))


def unload_ipython_extension(ipython) -> None:  # type: ignore[no-untyped-def]
    """Clean up by removing the registered cell magic."""
    if "d2" in ipython.magics_manager.cell_magics:
        del ipython.magics_manager.cell_magics["d2"]
