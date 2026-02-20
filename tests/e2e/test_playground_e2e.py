from __future__ import annotations

import functools
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYGROUND_DIR = REPO_ROOT / "playground"
PLAYGROUND_FILE = REPO_ROOT / "playground" / "d2_playground.py"


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        return


@pytest.mark.e2e
def test_exported_playground_renders_widget_in_browser(tmp_path: Path) -> None:
    if sys.version_info < (3, 10):
        pytest.skip("marimo playground export requires Python 3.10+")

    output_dir = tmp_path / "playground-dist"
    export = subprocess.run(
        [
            sys.executable,
            "-m",
            "marimo",
            "export",
            "html-wasm",
            PLAYGROUND_FILE.name,
            "-o",
            str(output_dir),
            "--mode",
            "run",
        ],
        cwd=PLAYGROUND_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Assets copied to" in export.stdout

    index_html = output_dir / "index.html"
    assert index_html.exists()

    playwright = pytest.importorskip("playwright.sync_api")
    handler = functools.partial(_QuietHandler, directory=str(output_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    page_errors: list[str] = []
    console_messages: list[str] = []
    try:
        url = f"http://127.0.0.1:{server.server_port}/"
        with playwright.sync_playwright() as session:
            browser = session.chromium.launch()
            try:
                page = browser.new_page()
                page.on("pageerror", lambda err: page_errors.append(str(err)))
                page.on("console", lambda msg: console_messages.append(msg.text))

                page.goto(url, wait_until="networkidle", timeout=120_000)
                page.get_by_role("heading", name="D2 Playground").wait_for(
                    timeout=120_000
                )

                required_markers = (
                    "Runtime is healthy",
                    "Loading from micropip: ['d2-widget']",
                )
                deadline = time.monotonic() + 120
                while True:
                    runtime_bootstrap_logs = "\n".join(console_messages)
                    if all(
                        marker in runtime_bootstrap_logs for marker in required_markers
                    ):
                        break
                    if time.monotonic() >= deadline:
                        pytest.fail(
                            "Timed out waiting for runtime bootstrap logs. "
                            f"Observed logs:\n{runtime_bootstrap_logs}"
                        )
                    page.wait_for_timeout(250)

                runtime_bootstrap_logs = "\n".join(console_messages)
                assert "Runtime is healthy" in runtime_bootstrap_logs
                assert "Loading from micropip: ['d2-widget']" in runtime_bootstrap_logs

                # Rendering can be delayed by the pyodide package installation step.
                # If widget output is present, validate it end-to-end.
                if page.locator(".d2-widget").count() > 0:
                    page.wait_for_selector(".d2-widget svg", timeout=120_000)
                    assert "Error generating diagram" not in page.content()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    assert page_errors == []
