import json


def extract_access_token_from_local_storage(page):
    keys = page.evaluate("Object.keys(window.localStorage)")
    for key in keys:
        if "auth0spajs" in key:
            try:
                raw_data = page.evaluate(f"window.localStorage.getItem('{key}')")
                parsed = json.loads(raw_data)
                if "body" in parsed and "access_token" in parsed["body"]:
                    return parsed["body"]["access_token"]
            except Exception:
                continue
    return None