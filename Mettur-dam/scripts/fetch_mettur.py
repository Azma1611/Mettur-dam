#!/usr/bin/env python3
"""
Fetch latest Mettur dam water level from Tamil Nadu reservoir status page
and append to data/data.json as {"date":"YYYY-MM-DD","level": <meters as float>}.

This attempts to parse the table row that contains "Mettur" (case-insensitive).
It prefers values labeled with 'm' or 'meter', and will convert 'ft'/'feet' -> meters.
If table parsing fails it will fall back to a page-wide regex search.

Edit SOURCE_URL if you prefer a different source.
"""
from pathlib import Path
from datetime import date
import requests
from bs4 import BeautifulSoup
import re
import json
import sys

# === Configure ===
SOURCE_URL = "https://www.tnagrisnet.tn.gov.in/home/reservoir/"
TIMEOUT = 20
USER_AGENT = "mettur-dam-bot/1.0 (+https://github.com/Azma1611/Mettur-dam)"
DATA_FILE = Path("data/data.json")
MAX_DAYS = 365
KEYWORD = "mettur"   # match row containing this keyword (case-insensitive)
# ==================

RE_FLOAT = re.compile(r"(-?\d{1,3}(?:\.\d+)?)")
RE_WITH_UNIT = re.compile(r"(-?\d{1,3}(?:\.\d+)?)(?:\s*)(m|meter|meters|ft|feet)?", re.I)

def fetch_html(url):
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text

def to_meters(value, unit_hint=None):
    """Convert numeric value to meters. If unit_hint contains 'ft', convert; otherwise assume meters."""
    try:
        v = float(value)
    except Exception:
        return None
    if unit_hint and re.search(r"ft|feet", unit_hint, re.I):
        return v * 0.3048
    # if unit explicitly 'm' treat as meters; otherwise guess:
    if unit_hint and re.search(r"m|meter", unit_hint, re.I):
        return v
    # Heuristic: values > 300 are probably in feet (unlikely meters); convert if >300
    if v > 300:
        return v * 0.3048
    # otherwise assume meters
    return v

def parse_row_for_level(tr):
    """Given a <tr>, return (level_in_meters, raw_value, unit_str) or (None, None, None)."""
    tds = tr.find_all(['td', 'th'])
    texts = [td.get_text(" ", strip=True) for td in tds]
    # Look for any explicit number+unit in the cell texts
    candidates = []
    for txt in texts:
        for m in RE_WITH_UNIT.finditer(txt):
            val = m.group(1)
            unit = m.group(2) or ""
            meters = to_meters(val, unit)
            if meters is not None:
                candidates.append((meters, val, unit, txt))
    if candidates:
        # Prefer candidate where unit indicates meters explicitly, else choose the most plausible:
        for c in candidates:
            if c[2] and re.search(r"m|meter", c[2], re.I):
                return c[0], c[1], c[2]
        # Otherwise prefer value closest to typical Mettur (~80 m) as heuristic
        candidates.sort(key=lambda x: abs(x[0]-80))
        return candidates[0][0], candidates[0][1], candidates[0][2]
    # fallback: any float in row
    for txt in texts:
        fm = RE_FLOAT.search(txt)
        if fm:
            meters = to_meters(fm.group(1), None)
            if meters is not None:
                return meters, fm.group(1), None
    return None, None, None

def find_mettur_in_tables(soup):
    # Search all table rows for the keyword
    for tr in soup.find_all('tr'):
        row_text = tr.get_text(" ", strip=True).lower()
        if KEYWORD.lower() in row_text:
            level_m, raw, unit = parse_row_for_level(tr)
            if level_m is not None:
                return level_m, raw, unit
    return None, None, None

def fallback_regex_search(text):
    # Search for patterns like 'Mettur ... 79.35 m' or 'Mettur - 79.35'
    pat = re.compile(r"mettur[^\d\n\r]{0,40}(-?\d{1,3}(?:\.\d+)?)(?:\s*)(m|meter|meters|ft|feet)?", re.I)
    m = pat.search(text)
    if m:
        val = m.group(1)
        unit = m.group(2) or ""
        meters = to_meters(val, unit)
        return meters, val, unit
    # another fallback: find 'Mettur' then nearest float in whole page
    idx = text.lower().find("mettur")
    if idx != -1:
        slice_text = text[idx:idx+200]
        m2 = RE_FLOAT.search(slice_text)
        if m2:
            val = m2.group(1)
            meters = to_meters(val, None)
            return meters, val, None
    return None, None, None

def load_existing():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_data(arr):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(arr, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    print("Fetching", SOURCE_URL)
    try:
        html = fetch_html(SOURCE_URL)
    except Exception as e:
        print("Failed to fetch source:", e, file=sys.stderr)
        sys.exit(2)

    soup = BeautifulSoup(html, "html.parser")
    level_m, raw, unit = find_mettur_in_tables(soup)
    if level_m is None:
        # try fallback regex on full text
        text = soup.get_text(" ", strip=True)
        level_m, raw, unit = fallback_regex_search(text)

    if level_m is None:
        print("ERROR: Could not parse Mettur level from source.", file=sys.stderr)
        sys.exit(3)

    print(f"Parsed level: {level_m:.3f} m (raw: {raw} {unit or ''})")
    today = date.today().isoformat()

    data = load_existing()
    # If last entry is today, update it; otherwise append
    if data and data[-1].get("date") == today:
        print("Replacing today's value")
        data[-1]["level"] = round(level_m, 3)
    else:
        data.append({"date": today, "level": round(level_m, 3)})

    # Keep only last MAX_DAYS entries
    if len(data) > MAX_DAYS:
        data = data[-MAX_DAYS:]

    save_data(data)
    print("Saved", len(data), "entries to", DATA_FILE)

if __name__ == "__main__":
    main()
