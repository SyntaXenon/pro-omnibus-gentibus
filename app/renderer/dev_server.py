"""Local dev server: serves the whole project as static files (so docs/*.html
can fetch content/*.json directly, e.g. hymns.json) AND adds one dynamic route,
GET /api/day?date=YYYY-MM-DD, that reruns the real day-construction logic in
render_day.py fresh on every request - reading straight from disk, no caching.

This is what makes "edit any content JSON, save, refresh the browser" work for
more than just hymns.json: the psalter tables, calendar cache, proper_texts,
and content/sanctorale/ all flow through resolve_and_build_day() same as the
static generator does, so there's exactly one implementation of that logic
(this file never reimplements it in JS) - only the freshness differs.

Usage: py app/renderer/dev_server.py [port]   (default port 8899)
Then open http://localhost:<port>/docs/demo_today.html - the page's own JS
already knows to prefer /api/day over its baked-in snapshot when it's reachable.
"""
import json
import sys
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

APP_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = APP_ROOT.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_day  # noqa: E402


def build_day_json(date_str: str) -> bytes | None:
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        return None
    # Force every cache render_day.py keeps at module level to re-read from
    # disk - a long-running server process would otherwise keep serving
    # whatever content/sanctorale/ looked like the first time it was scanned.
    render_day._sanctorale_index_cache = None
    corpora = {lang: render_day.BibleCorpus(lang) for lang in render_day.LANGUAGES}
    proper = {lang: render_day.ProperTextLibrary(lang) for lang in render_day.LANGUAGES}
    payload = render_day.build_date_payload(d, corpora, proper)
    if payload is None:
        return None
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/day":
            qs = parse_qs(parsed.query)
            date_str = (qs.get("date") or [""])[0]
            body = build_day_json(date_str) if date_str else None
            if body is None:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b"null")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet; errors still surface via response codes


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8899
    handler = partial(Handler, directory=str(PROJECT_ROOT))
    with ThreadingHTTPServer(("", port), handler) as httpd:
        print(f"Serving {PROJECT_ROOT} at http://localhost:{port}/  (Ctrl+C to stop)")
        print(f"Demo: http://localhost:{port}/docs/demo_today.html")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
