# Task Assignment: BOT-004 - Encrypt Timeline Entry Descriptions (HIPAA Compliance)

**Assigned to:** BOT-004
**Assigned by:** Q33N
**Priority:** P0 - SECURITY/COMPLIANCE REQUIREMENT
**Deadline:** 2025-11-01 19:00 CDT
**Scope:** FamilyBondBot Backend Encryption
**Depends On:** BOT-003 (can work in parallel or after, but pattern established by BOT-003)

---

## Task

Timeline entries contain sensitive incident/event descriptions that must be encrypted at rest per HIPAA requirements. Currently stored in plaintext in the database. Your job is to encrypt the entry descriptions using the existing EncryptionService - using the same pattern BOT-003 applies to coaching messages.

**What needs encryption:**
- `TimelineEntry.description` column - User's narrative of the event
- `TimelineEntry.notes` column (if exists) - Any additional notes
- Must support existing queries and retrieval
- Must maintain backward compatibility

---

## Success Criteria

- [ ] `TimelineEntry.description` is encrypted when stored
- [ ] `TimelineEntry.notes` (if exists) is encrypted when stored
- [ ] Content is automatically decrypted on retrieval
- [ ] All timeline-related integration tests pass
- [ ] Contract tests for timeline endpoints pass
- [ ] TimelinePage React component still displays entries correctly
- [ ] Add/edit/delete functionality works with encrypted data
- [ ] No performance regression
- [ ] Existing unencrypted entries can still be read (graceful degradation)
- [ ] Code is documented with docstrings

---

## Locations to Check

**Working Directory:**
```
C:\Users\davee\onedrive\documents\github\familybondbot\fbb
```

**Files to Modify:**
1. `backend/src/models/timeline_entry.py` - Model definition
2. `backend/src/services/encryption_service.py` - Already exists, just reference it
3. `backend/src/api/timeline.py` - API endpoints (if exists)
4. `backend/src/services/timeline_service.py` - Service layer (if exists)

**Reference Implementation:**
- `backend/src/models/coaching_message.py` - BOT-003 will have just encrypted this using same pattern
- Use BOT-003's work as your template

**Frontend Reference:**
- `frontend/src/pages/TimelinePage.tsx` - Verify it displays entries correctly
- Should work transparently (decryption happens on backend)

**Test Files to Verify:**
- `backend/tests/integration/test_e2e_critical_flows.py`
- Any timeline-specific tests

---

## How to Execute

### Step 1: Understand the Pattern from BOT-003
Read the completed task from BOT-003:
```
C:\Users\davee\onedrive\documents\github\deiasolutions\.deia\hive\responses\bot-003-ENCRYPT-MESSAGES-complete.md
```
Study the pattern they use for CoachingMessage - you'll use identical approach for TimelineEntry.

### Step 2: Examine TimelineEntry Model
```bash
cd C:\Users\davee\onedrive\documents\github\familybondbot\fbb
cat backend/src/models/timeline_entry.py | head -50
```
Identify:
- `description` field definition
- `notes` field (if exists) definition
- Any other text fields needing encryption
- Current relationships and constraints

### Step 3: Check for Query Dependencies
```bash
grep -r "TimelineEntry.*description\|timeline.*description" backend/src --include="*.py"
```
Ensure no queries search on `description` field (encrypted fields can't be efficiently queried).

### Step 4: Modify TimelineEntry Model
Apply the same pattern as BOT-003:
- Rename storage column with underscore prefix: `_description`, `_notes`
- Add `@property` decorators for encryption/decryption
- Import and use EncryptionService
- Add docstrings

**Pattern (identical to BOT-003's coaching messages):**
```python
from src.services.encryption_service import EncryptionService

class TimelineEntry(Base):
    __tablename__ = "timeline_entries"

    id = Column(Integer, primary_key=True)
    _description = Column("description", String, nullable=False)
    _notes = Column("notes", String, nullable=True)
    entry_type = Column(String, nullable=False)  # Not encrypted
    occurred_at = Column(DateTime, nullable=False)  # Not encrypted

    @property
    def description(self) -> str:
        """Decrypt description on read"""
        if self._description:
            return EncryptionService.decrypt(self._description)
        return ""

    @description.setter
    def description(self, value: str):
        """Encrypt description on write"""
        if value:
            self._description = EncryptionService.encrypt(value)
        else:
            self._description = ""

    @property
    def notes(self) -> str:
        """Decrypt notes on read"""
        if self._notes:
            return EncryptionService.decrypt(self._notes)
        return ""

    @notes.setter
    def notes(self, value: str):
        """Encrypt notes on write"""
        if value:
            self._notes = EncryptionService.encrypt(value)
        else:
            self._notes = ""
```

### Step 5: Check TimelineService/API
```bash
cat backend/src/api/timeline.py
cat backend/src/services/timeline_service.py (if exists)
```
Verify they use model properties correctly. No changes needed if they read/write via model.

### Step 6: Create Database Migration
```bash
cd backend
python -m alembic revision --autogenerate -m "encrypt_timeline_entry_descriptions"
```

### Step 7: Run Timeline Tests
```bash
cd backend
python -m pytest tests/integration/test_e2e_critical_flows.py -v --tb=short -k timeline
python -m pytest tests/contract/ -v --tb=short -k timeline (if any)
```
All should pass with encrypted content working transparently.

### Step 8: Verify Frontend Still Works
- TimelinePage should display entries correctly (decryption is transparent)
- Add/edit/delete operations should work
- Export should include decrypted descriptions
- No frontend changes needed if backend encryption is transparent

---

## Rules

1. **Follow BOT-003's pattern exactly** - Consistency is critical
2. **Use existing EncryptionService** - No new crypto code
3. **Encrypt text fields only** - Not dates, IDs, or enums
4. **Transparent to consumers** - API and frontend don't change
5. **Tests must pass** - All timeline tests work with encryption
6. **Document the approach** - Add docstrings explaining encryption

---

## Deliverable Format

Create a response file at:
```
C:\Users\davee\onedrive\documents\github\deiasolutions\.deia\hive\responses\bot-004-ENCRYPT-TIMELINE-complete.md
```

Include:
- [x] Status: COMPLETE or BLOCKED
- Files modified with line numbers
- Fields encrypted (description, notes, etc)
- Migration file created (name)
- Test results (pytest output)
- Frontend verification (TimelinePage still works)
- Any issues encountered
- Time spent

---

## Notes

- This task can start in parallel with BOT-003 (different model)
- Use BOT-003's work as reference template
- EncryptionService is battle-tested (already used for Parent model)
- Both encryption tasks (messages + timeline) needed before beta launch
- After this, the platform is HIPAA-ready for sensitive data

---

**Parallel:** Can work while BOT-003 is working (different files)
**Reference:** BOT-003's approach to coaching_message.py encryption
**Next:** Integration tests and final verification
