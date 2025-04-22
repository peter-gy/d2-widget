import pathlib
from typing import Optional

import anywidget
import traitlets

from d2_widget._model import CompileOptions

# These defaults ensure that multi-layer, animated diagrams are rendered by default.
DEFAULT_OPTIONS: CompileOptions = {
    "noXMLTag": True,
    "target": "*",
    "animateInterval": 1500,
    "pad": 25,
}


class Widget(anywidget.AnyWidget):
    """An `anywidget.AnyWidget` wrapper for D2 diagrams.

    This widget allows you to render D2 diagrams in Jupyter notebooks and other
    compatible environments.

    D2 is a modern diagram scripting language that turns text to diagrams.
    You can read about D2 diagrams at `https://d2lang.com <https://d2lang.com>`_ and access an
    online playground at `https://play.d2lang.com <https://play.d2lang.com>`_.
    """

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    _svg = traitlets.Unicode().tag(sync=True)
    diagram = traitlets.Unicode().tag(sync=True)
    options = traitlets.Dict().tag(sync=True)

    def __init__(self, diagram: str, options: Optional[CompileOptions] = None):
        """Initializes a Widget.

        Args:
            diagram (str): The diagram script to render.
            options (Optional[CompileOptions]): The options to use for rendering.
        """
        super().__init__()
        self.diagram = diagram
        self.options = DEFAULT_OPTIONS if options is None else options

    @property
    def svg(self) -> str:
        """The SVG representation of the diagram.

        This property might not be immediately up to date if accessed very shortly
        after the widget was rendered. Ensure to access the property only after
        the widget has been rendered in your notebook environment.

        Returns:
            str: The SVG representation of the diagram.
        """
        return self._svg
