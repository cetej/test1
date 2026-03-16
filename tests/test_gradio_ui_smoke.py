"""
Smoke tests for Pyramid Flow Gradio UI using Browser Use.

These tests verify that the Gradio interface loads correctly and UI elements
are accessible. They do NOT run actual video generation (which requires GPU).

Requirements:
    pip install browser-use langchain-anthropic pytest pytest-asyncio

Usage:
    # Start the Gradio app first (or use a running instance)
    # Then run:
    pytest tests/test_gradio_ui_smoke.py -v

    # Or with a custom URL:
    GRADIO_URL=http://localhost:7860 pytest tests/test_gradio_ui_smoke.py -v

Environment variables:
    GRADIO_URL: URL of the running Gradio app (default: http://localhost:7860)
    ANTHROPIC_API_KEY: Required for Browser Use agent
"""

import asyncio
import os

import pytest
import pytest_asyncio
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

GRADIO_URL = os.environ.get("GRADIO_URL", "http://localhost:7860")
LLM = ChatAnthropic(model="claude-sonnet-4-6")


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_gradio_app_loads():
    """Verify the Gradio app loads and shows the main title."""
    agent = Agent(
        task=f"""
        Go to {GRADIO_URL}.
        Check if the page loads and contains the text "Pyramid Flow Video Generation Demo".
        Report SUCCESS if you see it, FAILURE if not.
        """,
        llm=LLM,
    )
    result = await agent.run()
    output = result.final_result().lower()
    assert "success" in output, f"Gradio app did not load correctly: {output}"


@pytest.mark.asyncio
async def test_text_to_video_tab_elements():
    """Verify the Text-to-Video tab has all required UI elements."""
    agent = Agent(
        task=f"""
        Go to {GRADIO_URL}.
        Click on the "Text-to-Video" tab if not already selected.
        Verify ALL of these elements are present:
        1. A text input labeled "Prompt"
        2. A slider labeled "Duration"
        3. A slider labeled "Guidance Scale"
        4. A slider labeled "Video Guidance Scale"
        5. A "Generate Video" button
        6. A resolution dropdown with "768p" and "384p" options
        Report SUCCESS if all elements are present, or list which are MISSING.
        """,
        llm=LLM,
    )
    result = await agent.run()
    output = result.final_result().lower()
    assert "success" in output, f"Missing UI elements: {output}"


@pytest.mark.asyncio
async def test_image_to_video_tab_elements():
    """Verify the Image-to-Video tab has all required UI elements."""
    agent = Agent(
        task=f"""
        Go to {GRADIO_URL}.
        Click on the "Image-to-Video" tab.
        Verify ALL of these elements are present:
        1. An image upload area labeled "Input Image"
        2. A text input labeled "Prompt"
        3. A slider labeled "Duration"
        4. A slider labeled "Video Guidance Scale"
        5. A "Generate Video" button
        Report SUCCESS if all elements are present, or list which are MISSING.
        """,
        llm=LLM,
    )
    result = await agent.run()
    output = result.final_result().lower()
    assert "success" in output, f"Missing UI elements: {output}"


@pytest.mark.asyncio
async def test_prompt_input_accepts_text():
    """Verify the prompt input field accepts text."""
    agent = Agent(
        task=f"""
        Go to {GRADIO_URL}.
        Click on the "Text-to-Video" tab.
        Type "A cat walking on the beach at sunset" into the prompt text field.
        Verify the text was entered successfully.
        Do NOT click Generate.
        Report SUCCESS if the text was entered, FAILURE if not.
        """,
        llm=LLM,
    )
    result = await agent.run()
    output = result.final_result().lower()
    assert "success" in output, f"Could not enter text in prompt: {output}"


@pytest.mark.asyncio
async def test_examples_are_visible():
    """Verify that example prompts are shown in the Text-to-Video tab."""
    agent = Agent(
        task=f"""
        Go to {GRADIO_URL}.
        Click on the "Text-to-Video" tab.
        Check if there are example prompts visible below the controls.
        Look for text mentioning "space man" or "Tokyo" or "chicken".
        Report SUCCESS if you see at least one example, FAILURE if not.
        """,
        llm=LLM,
    )
    result = await agent.run()
    output = result.final_result().lower()
    assert "success" in output, f"Examples not visible: {output}"
