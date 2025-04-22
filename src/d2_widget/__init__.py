from d2_widget._version import __version__
from d2_widget._widget import Widget
from d2_widget._utils import parse_magic_arguments

__all__ = ["Widget", "__version__"]


def load_ipython_extension(ipython) -> None:  # type: ignore[no-untyped-def]
    """Extend IPython with interactive D2 widget display when using the `%d2` magic command."""
    from IPython.display import display
    from IPython.core.magic import register_cell_magic

    @register_cell_magic
    def d2(line, cell):
        options = parse_magic_arguments(line)
        display(Widget(cell, options))


def unload_ipython_extension(ipython) -> None:  # type: ignore[no-untyped-def]
    """Clean up by removing the registered cell magic."""
    if "d2" in ipython.magics_manager.cell_magics:
        del ipython.magics_manager.cell_magics["d2"]
