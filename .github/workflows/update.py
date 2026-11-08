import json, re, time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parents[1]
now = datetime.now(ZoneInfo("America/Costa_Rica"))
day = now.date().isoformat()
clock = re.compile(r"(?<!\d)(\d{1,2}):(\d{2})\s*([ap]\.?\s*m\.?)?", re.I)
session = requests.Session()
session.headers.update({"User-Agent": "PersonalTVGuidePilot/0.1 (personal schedule reader)"})

def minutes(value):
    match = clock.search(value)
    if not match:
        return None
    h, m = int(match[1]), int(match[2])
    suffix = (match[3] or "").lower().replace(".", "").replace(" ", "")
    if m > 59 or h > 23 or (suffix and not 1 <= h <= 12):
        return None
    if suffix:
        h = h % 12 + (12 if suffix == "pm" else 0)
    return f"{h:02}:{m:02}"

def extract(html):
    soup = BeautifulSoup(html, "html.parser")
    programs, seen = [], set()
    for row in soup.select("tr"):
        cells = row.find_all(["td", "th"], recursive=False)
        if len(cells) < 2:
            continue
        values = [c.get_text(" ", strip=True) for c in cells]
        # Only accept explicit time columns; never infer from unrelated page numbers.
        start = minutes(values[0]) if len(values[0]) < 24 else None
        if not start:
            continue
        end = minutes(values[1]) if len(values[1]) < 24 else None
        content = cells[2:] if end else cells[1:]
        if not content:
            continue
        links = [a.get_text(" ", strip=True) for c in content for a in c.select("a[href*='/programa/'], a[href*='/pelicula/'], a[href*='/serie/']")]
        title = next((x for x in links if x), content[0].get_text(" ", strip=True).split("\n")[0])
        if not title or len(title) > 300:
            continue
        key = (start, end, title)
        if key not in seen:
            programs.append({"start": start, "end": end, "title": title})
            seen.add(key)
    return programs

results = []
for config in json.loads((BASE / "channels.json").read_text(encoding="utf-8")):
    item = {**config, "date": day, "checked_at": now.isoformat(), "programs": [], "status": "error", "message": ""}
    url = config["url"].rstrip("/") + "/" + day
    item["source_url"] = url
    try:
        response = session.get(url, timeout=35)
        response.raise_for_status()
        if day not in response.url:
            raise ValueError("La fuente redirigió fuera de la fecha solicitada")
        programs = extract(response.text)
        item["programs"] = programs
        item["status"] = "unverified" if programs else "empty"
        item["message"] = ("Extracción experimental: fecha, señal, títulos y zona horaria pendientes de revisión." if programs else "No se encontraron filas con horarios. Puede requerir adaptar el extractor.")
    except Exception as exc:
        item["message"] = str(exc)[:250]
    results.append(item)
    time.sleep(3)
output = BASE / "site" / "data.json"
output.write_text(json.dumps({"updated_at": now.isoformat(), "channels": results}, ensure_ascii=False, indent=2), encoding="utf-8")
