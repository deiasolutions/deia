from pathlib import Path
import json, sys
sys.path.insert(0, str(Path.cwd()/'src'))
from deia.logger import quick_log
payload = json.loads(Path(r'.\\.deia\\temp\\log_session_payload.json').read_text(encoding='utf-8-sig'))
log_path = quick_log(
    context=payload['context'],
    transcript=payload['transcript'],
    decisions=payload['decisions'],
    action_items=payload['action_items'],
    files_modified=payload['files_modified'],
    next_steps=payload['next_steps'],
    status=payload.get('status','Active')
)
print(log_path)
