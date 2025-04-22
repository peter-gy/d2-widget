import importlib.metadata

try:
    __version__ = importlib.metadata.version("d2-widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
