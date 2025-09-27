import asyncio
import re
from typing import Any
from playwright.async_api import Page, WebSocket
from tests.components.ui.pages.base_page import BasePage


class ShellAppPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._output: list[str] = []

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")

        return (
            "Welcome to Apolo!" in self._output
            and "You are already logged in." in self._output
        )

    async def open_app(self, url: str) -> None:
        output_future = asyncio.create_task(self._capture_canvas_output(5000))
        await self.page.goto(url)

        self._output = await output_future

    async def enter_command(self, command: str) -> None:
        await self.page.keyboard.type(command)
        await self.page.keyboard.press("Enter")
        await self.page.wait_for_timeout(3000)

    async def check_output_line(self, value: str) -> bool:
        if value in self._output:
            return True
        else:
            return any(value in output_line for output_line in self._output)

    async def _capture_canvas_output(self, duration: int = 5000) -> list[str]:
        ANSI_ESCAPE = re.compile(
            r"""
            (?:\x1B[@-Z\\-_])              |  # ESC + single char
            (?:\x1B\[ [0-?]* [ -/]* [@-~]) |  # CSI ... sequence
            (?:\x1B\] .*? (?:\x07|\x1B\\))    # OSC ... BEL or ST
            """,
            re.VERBOSE,
        )

        def _strip_ansi(text: str) -> str:
            return ANSI_ESCAPE.sub("", text)

        messages: list[str] = []

        def _on_frame(payload: Any) -> None:
            if isinstance(payload, bytes):
                try:
                    payload = payload.decode("utf-8", errors="ignore")
                except Exception:
                    return
            else:
                return

            cleaned = _strip_ansi(payload).strip()
            print("[DEBUG] Cleaned frame:", repr(cleaned))

            if cleaned:
                messages.append(cleaned)
            else:
                print("[DEBUG] Frame discarded (empty after cleaning)")

        def _on_websocket(ws: WebSocket) -> None:
            print("[DEBUG] WebSocket opened:", ws.url)
            ws.on("framereceived", _on_frame)

        self.page.on("websocket", _on_websocket)

        await self.page.wait_for_timeout(duration)

        raw_output = "\n".join(messages)
        return self._filter_ascii_part(raw_output)

    def _filter_ascii_part(self, text: str) -> list[str]:
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if re.fullmatch(r"[@#*+=\-.:\s]+", stripped):
                continue

            alnum = sum(c.isalnum() for c in stripped)
            if alnum / max(len(stripped), 1) < 0.2:
                continue

            if stripped in {"0;", "1;", "2;"} or "\x07" in stripped:
                continue

            cleaned_lines.append(stripped)

        return cleaned_lines
