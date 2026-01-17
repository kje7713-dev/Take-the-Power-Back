#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Dict

SPEC_NAME = "file-social"
SPEC_VERSION = "0.1"

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "spec" / "examples"

ALLOWED_TYPES = {"profile", "post", "comment"}

def fail(msg: str) -> None:
    print(f"❌ {msg}")
    sys.exit(1)

def ok(msg: str) -> None:
    print(f"✅ {msg}")

def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"{path}: invalid JSON ({e})")

def require(obj: Dict[str, Any], key: str, path: Path) -> None:
    if key not in obj:
        fail(f"{path}: missing required field '{key}'")

def validate_envelope(obj: Dict[str, Any], path: Path) -> None:
    require(obj, "spec", path)
    require(obj, "type", path)
    require(obj, "id", path)
    require(obj, "created_at", path)

    spec = obj["spec"]
    if not isinstance(spec, dict):
        fail(f"{path}: 'spec' must be an object")

    if spec.get("name") != SPEC_NAME:
        fail(f"{path}: spec.name must be '{SPEC_NAME}'")
    if spec.get("version") != SPEC_VERSION:
        fail(f"{path}: spec.version must be '{SPEC_VERSION}'")

    t = obj["type"]
    if t not in ALLOWED_TYPES:
        fail(f"{path}: type must be one of {sorted(ALLOWED_TYPES)}")

def validate_media_ref(m: Dict[str, Any], path: Path) -> None:
    for k in ("media_id", "mime"):
        if k not in m:
            fail(f"{path}: MediaRef missing '{k}'")

    has_path = isinstance(m.get("path"), str) and m.get("path") != ""
    has_url = isinstance(m.get("url"), str) and m.get("url") != ""

    # exactly one of path or url
    if has_path == has_url:
        fail(f"{path}: MediaRef must include exactly one of 'path' or 'url'")

    if has_path and m["path"].startswith("/"):
        fail(f"{path}: MediaRef.path must be a relative path")

    if has_url and not (m["url"].startswith("http://") or m["url"].startswith("https://")):
        fail(f"{path}: MediaRef.url must be an absolute http(s) URL")

def validate_profile(obj: Dict[str, Any], path: Path) -> None:
    for k in ("display_name", "handle"):
        require(obj, k, path)

    avatar = obj.get("avatar")
    if avatar is not None:
        if not isinstance(avatar, dict):
            fail(f"{path}: avatar must be an object")
        validate_media_ref(avatar, path)

def validate_post(obj: Dict[str, Any], path: Path) -> None:
    # tombstones are allowed to omit most fields
    if obj.get("deleted") is True:
        require(obj, "updated_at", path)
        return

    for k in ("author_id", "visibility", "content"):
        require(obj, k, path)

    if not isinstance(obj["content"], dict):
        fail(f"{path}: content must be an object")

    attachments = obj.get("attachments", [])
    if attachments is None:
        attachments = []
    if not isinstance(attachments, list):
        fail(f"{path}: attachments must be an array")

    for a in attachments:
        if not isinstance(a, dict):
            fail(f"{path}: attachment must be an object")
        validate_media_ref(a, path)

def validate_comment(obj: Dict[str, Any], path: Path) -> None:
    if obj.get("deleted") is True:
        require(obj, "updated_at", path)
        return

    for k in ("author_id", "parent", "content"):
        require(obj, k, path)

    parent = obj["parent"]
    if not isinstance(parent, dict):
        fail(f"{path}: parent must be an object")
    for k in ("type", "id"):
        require(parent, k, path)

    if not isinstance(obj["content"], dict):
        fail(f"{path}: content must be an object")

def main() -> None:
    if not EXAMPLES_DIR.exists():
        fail(f"Missing examples directory: {EXAMPLES_DIR}")

    files = sorted(EXAMPLES_DIR.rglob("*.json"))
    if not files:
        fail(f"No example JSON files found under {EXAMPLES_DIR}")

    ok(f"Found {len(files)} example JSON files")

    for f in files:
        obj = load_json(f)
        if not isinstance(obj, dict):
            fail(f"{f}: top-level JSON must be an object")

        validate_envelope(obj, f)

        t = obj["type"]
        if t == "profile":
            validate_profile(obj, f)
        elif t == "post":
            validate_post(obj, f)
        elif t == "comment":
            validate_comment(obj, f)

    ok("All examples validated successfully")

if __name__ == "__main__":
    main()
