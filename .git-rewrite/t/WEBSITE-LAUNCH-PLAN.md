# Q33N Platform - Website Launch Plan

**Created:** 2025-10-16
**Strategy:** Q33N as AI coordination hosting platform
**Domains:** 5 domains, single-host architecture

---

## ✅ What We Built

### Structure Created
```
website/
├── config.yaml              ✅ Hugo configuration
├── content/
│   ├── _index.md            ✅ Q33N homepage
│   ├── deia/_index.md       ✅ DEIA section
│   ├── simdecisions/_index.md ✅ SimDecisions section
│   └── efemera/_index.md    ✅ Efemera section
├── layouts/
│   ├── _default/            ✅ Base templates
│   ├── index.html           ✅ Homepage layout
│   └── partials/            ✅ Header/footer
├── static/css/main.css      ✅ Styling
└── README.md                ✅ Deployment guide

netlify.toml                 ✅ Domain routing config
```

---

## 🎯 Strategic Positioning

### Q33N as Platform (Not Project)

**Before this session:**
> "DEIA is an AI coordination framework with some demos"

**After this session:**
> "Q33N is AI coordination hosting. DEIA, SimDecisions, and Efemera all run on it. You can too."

**This shifts you from:**
- Project → Platform
- Concept → Infrastructure
- Services → Product

---

## 🌐 Domain Strategy

### Primary: q33n.com
**Position:** AI Coordination Hosting Platform
**Message:** "Where AI Queens Coordinate"
**Audience:** Developers, businesses, AI engineers

### Forwarded Domains:
1. **deiasolutions.org/.com** → `q33n.com/deia/`
   - "Powered by Q33N"
   - Open-source framework

2. **simdecisions.com** → `q33n.com/simdecisions/`
   - "Hosted on Q33N"
   - Democracy simulation

3. **efemera.live** → `q33n.com/efemera/`
   - "Built with Queens"
   - Neural incubator experiments

**All domains show their original URL to visitors (Netlify proxy rewrite).**

---

## 🚀 Launch Sequence

### Phase 1: Infrastructure Setup (Now)
- [x] Hugo site structure created
- [x] Sample content for all sections
- [x] Netlify configuration
- [ ] Test build locally
- [ ] Deploy to Netlify
- [ ] Add all 5 domains
- [ ] Update DNS

**Timeline:** 1-2 days

---

### Phase 2: Content Expansion (Week 1-2)
- [ ] Expand Q33N homepage (features, pricing details)
- [ ] Add /docs/ section (getting started guides)
- [ ] Write DEIA documentation pages
- [ ] Add SimDecisions methodology page
- [ ] Create Efemera game showcase

**Goal:** Each site has 5-10 pages of real content

---

### Phase 3: Public Launch (Week 3-4)
- [ ] Announce Q33N platform
- [ ] Publish launch article ("Introducing Q33N")
- [ ] Social media campaign
- [ ] Submit to Product Hunt / Hacker News
- [ ] Email existing DEIA community

**Goal:** Get first 100 visitors, collect feedback

---

### Phase 4: Commercial Validation (Month 2-3)
- [ ] Add signup/login (Auth0 or Clerk)
- [ ] Create dashboard mockup
- [ ] Launch beta program
- [ ] Get first paying customer
- [ ] Iterate based on feedback

**Goal:** Validate that people will pay for AI coordination hosting

---

## 📝 Content Priorities

### Must Write Before Launch:

**Q33N (q33n.com):**
- [ ] /features/ - What Q33N provides
- [ ] /pricing/ - Tiers (Free/Pro/Enterprise)
- [ ] /docs/quickstart/ - 5-minute getting started
- [ ] /docs/deploy/ - Deploy your first Queen
- [ ] /enterprise/ - Enterprise offering

**DEIA (/deia/):**
- [ ] /deia/docs/architecture/ - System overview
- [ ] /deia/docs/protocols/ - Pheromone-RSM, QEE
- [ ] /deia/bok/ - Book of Knowledge index
- [ ] /deia/community/ - How to contribute

**SimDecisions (/simdecisions/):**
- [ ] /simdecisions/methodology/ - How simulations work
- [ ] /simdecisions/demo/ - Interactive demo or video
- [ ] /simdecisions/beta/ - Beta signup form

**Efemera (/efemera/):**
- [ ] /efemera/games/ - Playable games list
- [ ] /efemera/devlog/ - Behind-the-scenes stories
- [ ] /efemera/neural-incubator/ - Vision explanation

---

## 🛠️ Technical Next Steps

### Immediate (This Week):
1. **Install Hugo**
   ```bash
   choco install hugo-extended -y
   ```

2. **Test local build**
   ```bash
   cd website
   hugo server -D
   ```

3. **Deploy to Netlify**
   - Connect GitHub repo
   - Set build command: `cd website && hugo --minify`
   - Deploy

4. **Add domains**
   - q33n.com (primary)
   - deiasolutions.org
   - deiasolutions.com
   - simdecisions.com
   - efemera.live

5. **Update DNS**
   - Option A: Use Netlify DNS (easiest)
   - Option B: Add A/CNAME records manually

---

### Short-term (Next 2 Weeks):

1. **Content expansion**
   - Write 5 key pages per section
   - Add images/diagrams
   - Create FAQ

2. **Visual polish**
   - Logo design (Q33N crown + neural network)
   - Section color schemes
   - Icon set

3. **SEO basics**
   - Meta descriptions
   - OpenGraph images
   - Sitemap

4. **Analytics**
   - Add Plausible or Google Analytics
   - Track key pages
   - Monitor domain routing

---

### Medium-term (Month 2-3):

1. **Interactive elements**
   - Queen deployment playground
   - Pheromone visualization
   - SimDecisions demo embed

2. **Blog launch**
   - /blog/ section
   - RSS feed
   - First 3-5 posts

3. **Community features**
   - Newsletter signup
   - Discord/Slack link
   - Contributor showcase

4. **Commercial infrastructure**
   - Signup flow
   - Dashboard (static mockup)
   - Pricing calculator

---

## 💰 Revenue Model (Future)

### Q33N Hosting Tiers:

**Community (Free)**
- Static sites only
- 1 Queen
- Community support
- Perfect for: OSS projects, experiments

**Professional ($49/month)**
- Dynamic sites
- 5 Queens
- API access
- Email support
- Perfect for: Indie developers, small teams

**Enterprise (Custom)**
- Unlimited Queens
- Private deployments
- White-label
- Dedicated support
- SLA guarantee
- Perfect for: Companies, agencies

---

## 🎯 Success Metrics

### Launch (Month 1):
- [ ] All 5 domains live
- [ ] 100+ unique visitors
- [ ] 10+ newsletter signups
- [ ] 1 piece of press coverage

### Growth (Month 3):
- [ ] 1,000+ unique visitors
- [ ] 100+ newsletter subscribers
- [ ] 10+ beta signups
- [ ] 1 paying customer

### Validation (Month 6):
- [ ] 10,000+ unique visitors
- [ ] 500+ newsletter subscribers
- [ ] 50+ beta users
- [ ] 10+ paying customers
- [ ] $500+ MRR

---

## 🚨 Critical Decisions Made

1. **Q33N is the platform, not DEIA**
   - DEIA is a project hosted on Q33N
   - Q33N is the commercial brand

2. **Single-host architecture (for now)**
   - All sites on q33n.com infrastructure
   - Can split out later when needed

3. **Netlify as primary host**
   - Simple, fast, free tier sufficient
   - No Cloudflare needed (yet)

4. **No code needed to launch**
   - Static site generator (Hugo)
   - Markdown content
   - Deploy from GitHub

5. **Dogfooding strategy**
   - Your sites prove Q33N works
   - "We host on our own platform"

---

## 📞 Next Actions (You)

### Today:
1. Review what was built (`website/` directory)
2. Install Hugo if needed
3. Test local build (`hugo server`)

### This Week:
1. Deploy to Netlify
2. Add all 5 domains
3. Update DNS
4. Verify all domains route correctly

### Next Week:
1. Expand content (5-10 pages per section)
2. Add logos and visuals
3. Write launch announcement
4. Prepare social media assets

---

## 🎉 What This Enables

### Short-term:
- **Professional web presence** across all domains
- **Single place to send people** (q33n.com)
- **Proof of concept** (your sites hosted on your platform)

### Medium-term:
- **Platform positioning** (not just a project)
- **Revenue opportunity** (hosting for others)
- **Venture narrative** ("AWS for AI coordination")

### Long-term:
- **Ecosystem play** (Q33N becomes standard)
- **Network effects** (more Queens → more value)
- **Exit potential** (infrastructure > consulting)

---

## 🧭 Strategic Clarity

**You're not building:**
- ❌ A consulting company (services)
- ❌ Another AI tool (saturated market)
- ❌ A framework library (low monetization)

**You're building:**
- ✅ **Infrastructure platform** (Q33N)
- ✅ **Coordination layer** (multi-AI orchestration)
- ✅ **Open ecosystem** (DEIA as OSS foundation)
- ✅ **Scalable product** (hosting + API)

---

**This is the path from project to platform.**

**From concept to company.**

**From Dave's experiments to an industry standard.**

---

*Built: 2025-10-16*
*Structure: Complete*
*Ready: For deployment*
*Potential: Massive*

Let's ship it. 🚀
