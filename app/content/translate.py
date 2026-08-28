"""Machine translation for expanding beyond manually-translated languages.

Uses Google's unofficial (undocumented, no API key) translation endpoint.
This is NOT the official paid Google Cloud Translation API - it's a
widely-used-but-unsupported endpoint that could change or start rate-limiting
without notice. Fine for draft/demo translation, not something to depend on
for a production release.

Any text produced by this module should be stored with a clear "machine
translation, not reviewed" flag, same transparency standard as every other
piece of content in this project. It is NOT a substitute for the manually
produced Spanish translations already in the project, which remain the
higher-quality baseline - this exists for expanding to languages that don't
have a manual translation yet.
"""
import json
import urllib.parse
import urllib.request

ENDPOINT = "https://translate.googleapis.com/translate_a/single"


def translate(text: str, source: str, target: str) -> str:
    params = {"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text}
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "".join(seg[0] for seg in data[0] if seg[0])


if __name__ == "__main__":
    sample = "Dominus in templo sancto suo, Dominus in caelo sedes eius."
    print("LA:", sample)
    print("ES (MT):", translate(sample, "la", "es"))
    print("EN (MT):", translate(sample, "la", "en"))
