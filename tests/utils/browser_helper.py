import json
from typing import Any

from playwright.async_api import Page


async def extract_access_token_from_local_storage(page: Page) -> Any:
    keys = await page.evaluate("Object.keys(window.localStorage)")
    for key in keys:
        if "auth0spajs" in key:
            try:
                raw_data = await page.evaluate(f"window.localStorage.getItem('{key}')")
                parsed = json.loads(raw_data)
                if "body" in parsed and "access_token" in parsed["body"]:
                    return parsed["body"]["access_token"]
            except Exception:
                continue
    return None
