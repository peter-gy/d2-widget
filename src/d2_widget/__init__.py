import importlib.metadata
import pathlib

import anywidget
import traitlets
from typing import TypedDict, Optional, Literal, Annotated

try:
    __version__ = importlib.metadata.version("d2-widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class RenderOptions(TypedDict, total=False):
    """A `TypedDict` containing options for rendering D2 diagrams.

    Matches `RenderOptions` TypeScript interface from `@terrastruct/d2 <https://www.npmjs.com/package/@terrastruct/d2#RenderOptions>`_.
    """

    sketch: Annotated[
        bool,
        "Enable sketch mode [default: false]",
    ]
    themeID: Annotated[
        int,
        "Theme ID to use [default: 0]",
    ]
    darkThemeID: Annotated[
        int,
        "Theme ID to use when client is in dark mode",
    ]
    center: Annotated[
        bool,
        "Center the SVG in the containing viewbox [default: false]",
    ]
    pad: Annotated[
        int,
        "Pixels padded around the rendered diagram [default: 100]",
    ]
    scale: Annotated[
        float,
        "Scale the output. E.g., 0.5 to halve the default size. The default will render SVG's that will fit to screen. Setting to 1 turns off SVG fitting to screen.",
    ]
    forceAppendix: Annotated[
        bool,
        "Adds an appendix for tooltips and links [default: false]",
    ]
    target: Annotated[
        str,
        "Target board/s to render. If target ends with '', it will be rendered with all of its scenarios, steps, and layers. Otherwise, only the target board will be rendered. E.g. target: 'layers.x.*' to render layer 'x' with all of its children. Pass '' to render all scenarios, steps, and layers. By default, only the root board is rendered. Multi-board outputs are currently only supported for animated SVGs and so animateInterval must be set to a value greater than 0 when targeting multiple boards.",
    ]
    animateInterval: Annotated[
        int,
        "If given, multiple boards are packaged as 1 SVG which transitions through each board at the interval (in milliseconds).",
    ]
    salt: Annotated[
        str,
        "Add a salt value to ensure the output uses unique IDs. This is useful when generating multiple identical diagrams to be included in the same HTML doc, so that duplicate IDs do not cause invalid HTML. The salt value is a string that will be appended to IDs in the output.",
    ]
    noXMLTag: Annotated[
        bool,
        "Omit XML tag (<?xml ...?>) from output SVG files. Useful when generating SVGs for direct HTML embedding.",
    ]


class CompileOptions(RenderOptions, total=False):
    """A `TypedDict` containing options for compiling D2 diagrams, extending `RenderOptions`.

    Matches `CompileOptions` TypeScript interface from `@terrastruct/d2 <https://www.npmjs.com/package/@terrastruct/d2#CompileOptions>`_.
    """

    layout: Annotated[
        Literal["dagre", "elk"],
        "Layout engine to use [default: 'dagre']",
    ]
    fontRegular: Annotated[
        bytes,
        "A byte array containing .ttf file to use for the regular font. If none provided, Source Sans Pro Regular is used.",
    ]
    fontItalic: Annotated[
        bytes,
        "A byte array containing .ttf file to use for the italic font. If none provided, Source Sans Pro Italic is used.",
    ]
    fontBold: Annotated[
        bytes,
        "A byte array containing .ttf file to use for the bold font. If none provided, Source Sans Pro Bold is used.",
    ]
    fontSemibold: Annotated[
        bytes,
        "A byte array containing .ttf file to use for the semibold font. If none provided, Source Sans Pro Semibold is used.",
    ]


# These defaults ensure that multi-layer, animated diagrams are rendered by default.
DEFAULT_OPTIONS: CompileOptions = {
    "noXMLTag": True,
    "target": "*",
    "animateInterval": 1500,
}


class D2Widget(anywidget.AnyWidget):
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
        """Initializes a D2Widget.

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
