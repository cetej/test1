"""
Verification test: confirms Playwright + Chromium work in this environment.
Uses plain Playwright (no AI/LLM needed) to test a local HTML page.

Usage:
    pytest tests/test_browser_use_setup.py -v
"""

import os
import tempfile

import pytest
from playwright.sync_api import sync_playwright

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <h1>Pyramid Flow Test</h1>
    <p>If you can read this, Playwright is working correctly.</p>
    <button id="test-btn">Click Me</button>
    <input id="test-input" type="text" placeholder="Type here">
</body>
</html>
"""


@pytest.fixture(scope="module")
def html_file():
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False
    ) as f:
        f.write(HTML_CONTENT)
        f.flush()
        yield f.name
    os.unlink(f.name)


def test_playwright_can_open_page(html_file):
    """Verify Playwright can open a local HTML page and read its content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{html_file}")

        heading = page.locator("h1").text_content()
        assert heading == "Pyramid Flow Test"

        button = page.locator("#test-btn")
        assert button.is_visible()
        assert button.text_content() == "Click Me"

        text_input = page.locator("#test-input")
        assert text_input.is_visible()
        text_input.fill("Hello from test")
        assert text_input.input_value() == "Hello from test"

        browser.close()


def test_playwright_takes_screenshot(html_file):
    """Verify Playwright can take a screenshot."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{html_file}")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img:
            page.screenshot(path=img.name)
            assert os.path.getsize(img.name) > 0
            os.unlink(img.name)

        browser.close()
