"""Збирає автономний index.html: вбудовує скріншоти з img/ як data:image/png;base64."""
import base64
import pathlib
import re

root = pathlib.Path(__file__).parent
src = (root / "src" / "index.src.html").read_text(encoding="utf-8")
cache = {}


def inline(m):
    name = m.group(1)
    if name not in cache:
        data = (root / "img" / name).read_bytes()
        cache[name] = "data:image/png;base64," + base64.b64encode(data).decode()
    return 'src="' + cache[name] + '"'


out = re.sub(r'src="img/([\w.-]+\.png)"', inline, src)
(root / "index.html").write_text(out, encoding="utf-8")
print(f"index.html: {len(out) / 1024:.0f} KB, вбудовано {len(cache)} скріншотів")
