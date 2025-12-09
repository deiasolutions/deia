# Task Assignment: BOT-003 - Encrypt Coaching Messages (HIPAA Compliance)

**Assigned to:** BOT-003
**Assigned by:** Q33N
**Priority:** P0 - SECURITY/COMPLIANCE REQUIREMENT
**Deadline:** 2025-11-01 18:00 CDT
**Scope:** FamilyBondBot Backend Encryption
**Depends On:** BOT-002 (test fixes must complete first)

---

## Task

Coaching messages contain sensitive clinical/family information and must be encrypted at rest per HIPAA requirements. Currently stored in plaintext in the database. Your job is to encrypt the message content using the existing EncryptionService.

**What needs encryption:**
- `CoachingMessage.content` column - The actual message text sent/received
- Must support existing queries and retrieval
- Must maintain backward compatibility with existing messages

---

## Success Criteria

- [ ] `CoachingMessage.content` is encrypted when stored
- [ ] Content is automatically decrypted on retrieval
- [ ] All existing integration tests pass (after BOT-002 fixes them)
- [ ] Contract tests for coaching endpoints pass
- [ ] No performance regression (queries still fast)
- [ ] Existing unencrypted messages can still be read (graceful degradation)
- [ ] New messages are encrypted by default
- [ ] Code is documented with docstrings

---

## Locations to Check

**Working Directory:**
```
C:\Users\davee\onedrive\documents\github\familybondbot\fbb
```

**Files to Modify:**
1. `backend/src/models/coaching_message.py` - Model definition
2. `backend/src/services/encryption_service.py` - Encryption logic (already exists)
3. `backend/src/services/coaching_service.py` - Service layer
4. `backend/src/api/coaching.py` - API endpoints (verify they work with encrypted content)

**Reference Implementation (already done for other fields):**
- `backend/src/models/parent.py` - Email, first_name, last_name are encrypted
- Look at how they use `Column(String, ...` with encrypted values

**Test Files to Verify:**
- `backend/tests/contract/test_coaching_messages_post.py` (after BOT-002 fixes it)
- `backend/tests/contract/test_coaching_sessions_get.py`
- `backend/tests/integration/test_coaching_flow.py` (after BOT-002 fixes it)

---

## How to Execute

### Step 1: Study Existing Encryption Pattern
```bash
cd C:\Users\davee\onedrive\documents\github\familybondbot\fbb
grep -n "email.*encrypted\|first_name.*encrypted" backend/src/models/parent.py
```
Understand how Parent model encrypts email/name fields. You'll see:
- Import statement for EncryptionService
- Property decorator pattern for encryption/decryption

### Step 2: Check CoachingMessage Model
```bash
cat backend/src/models/coaching_message.py | head -50
```
Identify:
- Current `content` field definition
- What needs to stay plaintext vs encrypted
- Any indexes or queries on content

### Step 3: Modify CoachingMessage Model
Update `backend/src/models/coaching_message.py`:
- Add private `_content` storage field
- Add `@property content` for decryption on read
- Add setter to encrypt on write
- Use EncryptionService (same pattern as Parent model)

**Pattern (from Parent model):**
```python
from src.services.encryption_service import EncryptionService

class CoachingMessage(Base):
    __tablename__ = "coaching_messages"

    id = Column(Integer, primary_key=True)
    _content = Column("content", String, nullable=False)  # Storage field
    session_id = Column(Integer, ForeignKey("coaching_sessions.id"))

    @property
    def content(self) -> str:
        """Decrypt content on read"""
        if self._content:
            return EncryptionService.decrypt(self._content)
        return ""

    @content.setter
    def content(self, value: str):
        """Encrypt content on write"""
        if value:
            self._content = EncryptionService.encrypt(value)
        else:
            self._content = ""
```

### Step 4: Update CoachingService
Check `backend/src/services/coaching_service.py`:
- Message creation (already calls model, should work)
- Message retrieval (verify content property is called)
- Message listing (verify each message decrypts)

No changes needed if service uses the model properties correctly.

### Step 5: Verify API Endpoints Still Work
Check `backend/src/api/coaching.py`:
- POST endpoint to create message (should encrypt via model)
- GET endpoints to retrieve messages (should decrypt via model property)

No changes needed if they use the model properties.

### Step 6: Create Database Migration
```bash
cd backend
python -m alembic revision --autogenerate -m "encrypt_coaching_message_content"
```
This will:
- Detect the column rename (_content)
- Create migration file
- Do NOT run the migration yet

### Step 7: Run Tests to Verify
```bash
cd backend
python -m pytest tests/contract/test_coaching_messages_post.py -v --tb=short
python -m pytest tests/contract/test_coaching_sessions_get.py -v --tb=short
```
Both should pass with encrypted content working transparently.

### Step 8: Verify Backward Compatibility
If there are existing unencrypted messages:
- Add try/except in the content property getter
- If decrypt fails, return the value as-is (graceful degradation)
- Log the issue for migration

---

## Rules

1. **Use existing EncryptionService** - Don't create new crypto code
2. **Transparent to API** - Consumers shouldn't know about encryption
3. **Tests must pass** - All existing coaching tests must still work
4. **No breaking changes** - Old code that reads messages still works
5. **Document the pattern** - Add docstring explaining encryption approach

---

## Deliverable Format

Create a response file at:
```
C:\Users\davee\onedrive\documents\github\deiasolutions\.deia\hive\responses\bot-003-ENCRYPT-MESSAGES-complete.md
```

Include:
- [x] Status: COMPLETE or BLOCKED
- Files modified with line numbers
- Migration file created (name)
- Test results (pytest output)
- Any issues encountered
- Time spent

---

## Notes

- This follows the same pattern already used for Parent.email, Parent.first_name, Parent.last_name
- EncryptionService is fully implemented and tested
- Migration will be applied by DevOps before deployment
- After completion, BOT-004 will do the same for timeline entries

---

**Blocking:** BOT-002 must complete first (test fixes needed)
**Next:** BOT-004 will encrypt timeline entries using same approach
