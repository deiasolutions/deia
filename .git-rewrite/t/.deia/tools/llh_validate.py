#!/usr/bin/env python3
"""
LLH/TAG/Egg Validator
Validates YAML front matter and schema for DEIA organizational entities.
Accepts alias fields across styles (Claude/OpenAI) and eOS manifests.
"""
import sys
import yaml
import json
import re
from pathlib import Path


def validate_entity(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        return {"ok": False, "errors": ["file_not_found"], "path": str(path)}

    content = path.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---\n"):
        return {"ok": False, "errors": ["missing_yaml_front_matter"], "path": str(path)}

    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return {"ok": False, "errors": ["invalid_yaml_structure"], "path": str(path)}

    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        return {"ok": False, "errors": [f"yaml_parse_error:{e}"], "path": str(path)}

    errors = []
    warnings = []

    # Normalize aliases
    kind = fm.get("type") or fm.get("kind") or ""
    name = fm.get("name") or fm.get("title") or ""
    created = fm.get("created") or fm.get("date") or ""
    status = fm.get("status") or "draft"
    # eOS presence informational
    if "eos" in fm:
        warnings.append("eos_manifest_present")

    # Required commons
    if not fm.get("id"):
        errors.append("missing:id")
    if not kind:
        errors.append("missing:type")
    if not name:
        warnings.append("missing:name/title")
    if not created:
        warnings.append("missing:created/date")

    # Type specific
    if kind == "llh":
        if "members" in fm and not isinstance(fm.get("members"), list):
            errors.append("invalid:members_must_be_list")
        if "governance" not in fm:
            warnings.append("missing:governance")
    elif kind == "tag":
        if "members" not in fm:
            errors.append("missing:members")
        if "ttl" not in fm:
            warnings.append("missing:ttl")
        if not (fm.get("mission") or fm.get("purpose")):
            warnings.append("missing:mission/purpose")
    elif kind == "egg":
        # accept either deia_routing or routing block
        if not (fm.get("deia_routing") or fm.get("routing")):
            warnings.append("missing:deia_routing/routing")
    else:
        errors.append(f"invalid_type:{kind}")

    # ID format warning
    if fm.get("id") and not re.fullmatch(r"[a-z0-9-]+", str(fm.get("id"))):
        warnings.append("id_not_kebab_case")

    return {
        "ok": len(errors) == 0,
        "entity_type": kind,
        "errors": errors,
        "warnings": warnings,
        "path": str(path),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: llh_validate.py <file-path> [more files...]")
        sys.exit(2)
    results = [validate_entity(p) for p in sys.argv[1:]]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    ok = all(r.get("ok") for r in results)
    sys.exit(0 if ok else 1)
