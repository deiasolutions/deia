from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


KB_PATH = Path(__file__).resolve().parent / "kb.json"
ALLOWED_TYPES = {"RULE", "SNIPPET"}
ALLOWED_DELIVERY = {"cache_prompt", "task_file", "both"}


def load_entities() -> List[Dict]:
    if not KB_PATH.exists():
        return []
    return json.loads(KB_PATH.read_text(encoding="utf-8"))


def save_entities(entities: List[Dict]) -> None:
    KB_PATH.write_text(json.dumps(entities, indent=2), encoding="utf-8")


def upsert_entity(entity: Dict) -> Dict:
    entities = load_entities()
    entity_id = entity.get("id")
    if not entity_id:
        raise ValueError("entity must include id")
    entity_type = entity.get("type")
    if entity_type not in ALLOWED_TYPES:
        raise ValueError(f"entity type must be one of {sorted(ALLOWED_TYPES)}")
    delivery_mode = entity.get("delivery_mode", "cache_prompt")
    if delivery_mode not in ALLOWED_DELIVERY:
        raise ValueError(f"delivery_mode must be one of {sorted(ALLOWED_DELIVERY)}")

    existing = [e for e in entities if e.get("id") == entity_id]
    if existing:
        entities = [e if e.get("id") != entity_id else entity for e in entities]
    else:
        entities.append(entity)

    save_entities(entities)
    return entity


def list_entities() -> List[Dict]:
    return load_entities()


def preview_injection(entity_ids: List[str]) -> str:
    entities = load_entities()
    selected = [e for e in entities if e.get("id") in entity_ids]
    blocks = []
    for e in selected:
        blocks.append(
            f"[RAQCOON {e.get('type', 'ENTITY')}]\n"
            f"Title: {e.get('title')}\n"
            f"Summary: {e.get('summary')}\n"
            f"Tags: {', '.join(e.get('tags', []))}\n"
        )
    return "\n".join(blocks)
