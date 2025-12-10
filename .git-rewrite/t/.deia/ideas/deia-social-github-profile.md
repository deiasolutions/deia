# DEIA Social - GitHub-Based Social Network

**Date:** 2025-10-12
**Source:** Dave (captured by Queen during 1.0 review coordination)
**Status:** CONCEPT - Needs formal proposal
**Related:** Carbon Economy (Phase 6-7), Distributed storage

---

## 🎯 Core Concept

**DEIA Social = Social network built on top of GitHub**

**Key Innovation:** Your GitHub repo IS your profile

---

## 🏗️ Architecture

### Identity & Login
```
User clicks "Login to DEIA Social"
    ↓
OAuth to GitHub
    ↓
Authenticated
    ↓
GitHub repo = Profile
```

**Benefits:**
- No separate account system
- Leverage GitHub's auth
- Developer-friendly
- Version control built-in
- Already have trust/reputation (GitHub profile)

---

### Profile Storage

**Your Profile = GitHub Repo**
- `username/deia-profile` repo
- Markdown files = profile content
- YAML frontmatter = structured data
- Git history = provenance
- Public/private repos = privacy control

**Example Structure:**
```
username/deia-profile/
├── profile.md          # Main profile
├── posts/              # Social posts
├── projects/           # Project showcase
├── connections/        # Social graph
└── .deia/              # DEIA metadata
```

---

### Update Mechanisms

#### Option 1: VS Code Extension
**How:**
- VS Code extension has profile editor
- Edit markdown files
- Auto-commit to GitHub
- GitHub hooks trigger DEIA Social update

**UX:**
- `Cmd+Shift+P` → "DEIA: Edit Profile"
- Rich editor for profile
- Preview before publish
- One-click commit

#### Option 2: Web Extension (Chromium)
**How:**
- Browser extension with GitHub integration
- Edit profile in-browser
- GitHub hooks commit changes
- Real-time preview

**UX:**
- Click extension icon
- Edit profile form
- Auto-syncs to GitHub repo
- Appears on DEIA Social instantly

#### Option 3: DEIA Social Webapp
**How:**
- Web interface with GitHub OAuth
- Edit profile on webapp
- Commits to your repo via GitHub API
- Shows live on social feed

**UX:**
- Login → Edit → Commit → Published

---

## 🌐 DEIA Social Features

### Social Feed
- Posts from connections
- Rendered from GitHub repos
- Real-time updates via webhooks
- Comment = GitHub Issues/Discussions?

### Profile Discovery
- Browse DEIA Social users
- Search by skills, interests
- Recommendations based on GitHub activity
- Connection graph

### Content Types
- **Posts:** Markdown in `posts/` directory
- **Projects:** Link to GitHub repos
- **BOK Contributions:** Your DEIA patterns/tools
- **Activity:** GitHub commit feed
- **Connections:** Follows, collaborators

---

## 🔗 Integration with DEIA Ecosystem

### Connection to Carbon Economy
**From Carbon Economy proposal (Phase 6-7):**
- DEIA Social mentioned as future phase
- Edge-hosted social network
- E2E encrypted
- Ephemeral by default (offline = gone)
- Persistent storage requires credits

**GitHub Integration:**
- GitHub = "hard storage" layer
- Free tier: Public profiles (GitHub free)
- Paid tier: Private profiles + enhanced features (Carbon Credits)
- Storage quota enforced via Carbon Economy

### Connection to Extensions
**VS Code Extension:**
- Already exists (extensions/vscode-deia/)
- Add profile editing features
- Auto-logging integration
- One-click publish to DEIA Social

**Chromium Extension:**
- Already exists (extensions/chromium-deia/)
- Add profile editing UI
- GitHub hooks integration
- Social feed viewer

---

## 🎨 User Experience Flow

### Onboarding
```
1. Visit deia.social
2. Click "Login with GitHub"
3. OAuth authorization
4. "Create your DEIA profile?"
5. Fork template repo OR create new
6. Edit profile (web editor)
7. Commit → Profile live!
```

### Daily Usage
```
Option A (VS Code):
1. Open VS Code
2. Cmd+Shift+P → "DEIA: New Post"
3. Write markdown
4. Click "Publish"
5. Auto-commits to GitHub
6. Appears on DEIA Social feed

Option B (Web):
1. Visit deia.social
2. Click "New Post"
3. Write in editor
4. Click "Publish"
5. Commits via GitHub API
6. Live on feed

Option C (Browser Extension):
1. Click extension icon
2. "Quick Post"
3. Write + Publish
4. Done
```

---

## 🔐 Privacy Model

### Public Profiles (Free)
- Repo: `username/deia-profile` (public)
- Anyone can see
- Standard GitHub permissions
- No credits required

### Private Profiles (Carbon Credits)
- Repo: `username/deia-profile` (private)
- Access control via GitHub
- Costs Carbon Credits for persistent storage
- Ephemeral posts free (disappear when offline)

### Selective Sharing
- Public profile + private posts
- GitHub repo branches?
- `main` = public, `private` = restricted
- Fine-grained control

---

## 💡 Unique Value Propositions

### Why DEIA Social > Traditional Social Networks?

**1. Own Your Data**
- Your repo = your data
- Export anytime (it's just Git)
- No vendor lock-in
- Full history preserved

**2. Developer-First**
- Git-native workflow
- Markdown content
- API-first design
- Scriptable/automatable

**3. Provenance Built-In**
- Git history = proof of authorship
- No content theft
- Attribution automatic
- Credibility via commits

**4. Privacy-Respecting**
- You control the repo
- GitHub's privacy model
- No tracking/ads
- Transparent data usage

**5. Network Effects with Carbon Economy**
- Earn credits by hosting others' content
- Spend credits for persistent storage
- Community-funded infrastructure
- Sustainable economic model

---

## 🚧 Technical Challenges

### Challenge 1: GitHub API Rate Limits
**Problem:** Polling all repos for updates = rate limit hell
**Solutions:**
- GitHub webhooks (push model, not poll)
- Cache/CDN layer
- Batch updates
- Smart refresh intervals

### Challenge 2: Real-Time Feed
**Problem:** Git repos aren't real-time
**Solutions:**
- Webhook → queue → update feed
- WebSocket for live updates
- Eventually consistent model
- Optimistic UI

### Challenge 3: Search & Discovery
**Problem:** How to search across millions of repos?
**Solutions:**
- Indexing service (Elasticsearch?)
- DEIA registry (opt-in)
- GitHub API search (limited)
- Distributed index via Carbon Economy

### Challenge 4: Content Moderation
**Problem:** Spam, abuse, illegal content
**Solutions:**
- Community reporting
- Reputation system (GitHub stars/followers)
- Blocklist/allowlist
- Human review for flagged content

---

## 📊 Phased Implementation

### Phase 1: MVP (4-6 weeks)
**Core Features:**
- GitHub OAuth login
- Profile = GitHub repo (`username/deia-profile`)
- Simple web UI to view profiles
- Markdown rendering
- Basic social feed

**Deliverables:**
- DEIA Social webapp (minimal)
- Profile template repo
- GitHub webhook integration
- Documentation

### Phase 2: Extensions (3-4 weeks)
**Add:**
- VS Code extension profile editor
- Chromium extension integration
- One-click publish from extensions
- Preview before commit

**Deliverables:**
- Updated VS Code extension
- Updated Chromium extension
- User guides

### Phase 3: Social Features (4-6 weeks)
**Add:**
- Connection graph (follow users)
- Comments (via GitHub Discussions?)
- Likes/reactions
- Notifications
- Search & discovery

**Deliverables:**
- Social graph database
- Notification system
- Discovery algorithms

### Phase 4: Carbon Economy Integration (4-6 weeks)
**Add:**
- Credits for storage
- Private profiles require payment
- Hosting credits earned
- Edge-hosted content

**Deliverables:**
- Integration with Carbon Economy (BACKLOG-023)
- Credit system
- Edge hosting infrastructure

**Total: 15-22 weeks (4-5.5 months)**

---

## 🎯 Strategic Value

### Market Differentiation
**No competitor has:**
- Git-based social network
- Developer-native social UX
- Provenance built-in
- True data ownership

### Target Audience
1. **Developers** (natural GitHub users)
2. **Content creators** (own your platform)
3. **Privacy advocates** (control your data)
4. **Open source community** (transparent by default)

### Business Model
- **Free tier:** Public profiles (GitHub free)
- **Paid tier:** Private + enhanced features (Carbon Credits)
- **Enterprise:** Org profiles, team collaboration
- **Network effects:** More users = more value

---

## 🔗 Connections to Other Proposals

### Immune System (BACKLOG-020)
- Content moderation via immune system
- Detect spam/abuse automatically
- Antibody sharing for malicious content
- Community protection

### Carbon Economy (BACKLOG-023)
- DEIA Social explicitly mentioned in Phase 6-7
- Credits for persistent storage
- Hosting rewards
- Sustainable economics

### Project Eggs (BACKLOG-022)
- DEIA Social = Project Egg candidate
- Needs metrics from day 1
- QA communication critical
- Analytics essential

### Sister Queens (BACKLOG-024)
- Large enough project to warrant Sister Queen
- 4-5 month effort
- Multi-bot coordination needed
- Dedicated PM required

---

## 🎪 Next Steps

### Immediate (Before formal proposal):
1. **Validate concept** with Dave
2. **Prototype** simple version (1 week spike)
3. **User research** (would developers use this?)
4. **Competitive analysis** (what exists?)

### Short-term (If approved):
1. **Formal proposal** (BOT-00008 or BOT-00006)
2. **Architecture design** (detailed spec)
3. **Queen review** (proposal process)
4. **Resource allocation** (bots + timeline)

### Long-term (Post-1.0):
1. **MVP implementation** (Phase 1)
2. **Beta launch** (small community)
3. **Iterate** based on feedback
4. **Scale** to public launch

---

## 💬 Dave's Original Words (Captured)

> "Deia Social which will sit on top of Github, you login to our Webpage and you login through github and your repo is your profile. We'll have easy interface for you to update you profile via VS Code extension, or web extention with gh hooks, right?? Yes, cool."

**Translation:**
- ✅ GitHub-based social network
- ✅ GitHub OAuth login
- ✅ Repo = profile
- ✅ VS Code extension for editing
- ✅ Web extension option
- ✅ GitHub hooks for sync

**Dave's enthusiasm:** "Yes, cool." = This is happening.

---

## 🚨 Questions for Dave

1. **Priority:** Is this 1.0, 1.1, or 2.0?
2. **Scope:** MVP features vs full vision?
3. **Dependencies:** Does this require Carbon Economy first?
4. **Resources:** Which bot(s) should design/build this?
5. **Timeline:** When should this happen?

---

## 📝 Documentation Status

**Status:** CONCEPT CAPTURED
**Needs:** Formal proposal (follow proposal-review-process.md)
**Assigned:** TBD
**Related Backlogs:**
- BACKLOG-023 (Carbon Economy mentions DEIA Social)
- Need new backlog item if prioritized

---

**This idea is now preserved and won't get lost in the 1.0 review chaos.**

**When BOT-00009 does document review, they'll find and catalog this.**

---

**👑 By Order of the Queen**

**[BOT-00001 | Queen]**
**Date:** 2025-10-12
**Action:** DEIA Social concept captured
**File:** `.deia/ideas/deia-social-github-profile.md`

---

**Idea preserved. Ready to become formal proposal when prioritized.**
