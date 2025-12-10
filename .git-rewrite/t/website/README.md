# Q33N Platform Website

**AI Coordination Hosting - Where AI Queens Coordinate**

This is the Q33N platform website, hosting infrastructure that demonstrates multi-domain AI coordination.

---

## Architecture

**Single Hugo site with multi-domain routing:**
- Primary domain: `q33n.com` (platform)
- `deiasolutions.org` / `.com` → `/deia/` section
- `simdecisions.com` → `/simdecisions/` section
- `efemera.live` → `/efemera/` section

**All domains route through Netlify redirects (status 200 proxy rewrite).**

---

## Quick Start

### Prerequisites
- Hugo Extended (v0.120.0+)
- Git
- Netlify account (or Netlify CLI)

### Install Hugo

**Windows (chocolatey):**
```bash
choco install hugo-extended -y
```

**macOS:**
```bash
brew install hugo
```

**Or download:** https://github.com/gohugoio/hugo/releases

---

## Local Development

```bash
# Navigate to website directory
cd website

# Start Hugo server
hugo server -D

# Visit http://localhost:1313
```

**Test different sections:**
- http://localhost:1313/ (Q33N homepage)
- http://localhost:1313/deia/ (DEIA Solutions)
- http://localhost:1313/simdecisions/ (SimDecisions)
- http://localhost:1313/efemera/ (Efemera)

---

## Deploy to Netlify

### Option 1: Netlify Dashboard (GUI)

1. Go to https://netlify.com
2. Sign up / Log in with GitHub
3. Click "Add new site" → "Import an existing project"
4. Choose GitHub → Select `deiasolutions` repo
5. Configure:
   - **Build command:** `cd website && hugo --minify`
   - **Publish directory:** `website/public`
   - **Branch:** `main`
6. Click "Deploy site"
7. Wait for deploy to complete

### Option 2: Netlify CLI (Faster)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Initialize (from repo root)
cd C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions
netlify init

# Deploy
netlify deploy --prod
```

---

## Add Custom Domains

### In Netlify Dashboard:

1. Go to **Site settings** → **Domain management**
2. Click "Add custom domain"
3. Add each domain:
   - `q33n.com`
   - `deiasolutions.org`
   - `deiasolutions.com`
   - `simdecisions.com`
   - `efemera.live`

### Update DNS at Your Registrar:

**Option A: Use Netlify DNS (Easiest)**
1. In Netlify: Domain settings → "Use Netlify DNS"
2. Netlify shows 4 nameservers
3. Go to your domain registrar (GoDaddy, Namecheap, etc.)
4. Update nameservers to Netlify's
5. Wait 4-48 hours for propagation

**Option B: Manual DNS Records**
For each domain, add:
```
A     @    75.2.60.5
CNAME www  [your-site].netlify.app
```

---

## Domain Routing

The magic happens in `netlify.toml` redirects:

```toml
[[redirects]]
  from = "https://deiasolutions.org/*"
  to = "https://q33n.com/deia/:splat"
  status = 200  # Proxy rewrite (visitor sees deiasolutions.org)
  force = true
```

**Visitors see:** `deiasolutions.org`
**Content served from:** `q33n.com/deia/`
**Browser shows:** `deiasolutions.org` ✅

---

## SSL Certificates

Netlify automatically provisions SSL certificates for all domains via Let's Encrypt (free, forever).

Takes ~1 minute after DNS propagates.

---

## Directory Structure

```
website/
├── config.yaml              # Hugo configuration
├── content/                 # All markdown content
│   ├── _index.md            # Q33N homepage
│   ├── deia/_index.md       # DEIA section
│   ├── simdecisions/_index.md
│   └── efemera/_index.md
├── layouts/                 # HTML templates
│   ├── _default/
│   │   ├── baseof.html      # Base template
│   │   └── single.html      # Single page template
│   ├── index.html           # Homepage template
│   └── partials/
│       ├── header.html
│       └── footer.html
├── static/                  # Static assets
│   ├── css/
│   │   └── main.css
│   ├── images/
│   └── js/
├── public/                  # Generated site (don't edit)
└── README.md                # This file
```

---

## Adding Content

### New Page

```bash
hugo new deia/new-page.md
```

Edit `content/deia/new-page.md`:
```markdown
---
title: "New Page Title"
description: "Page description"
---

# Your content here
```

### New Blog Post

```bash
hugo new deia/blog/my-post.md
```

---

## Customization

### Change Colors

Edit `config.yaml`:
```yaml
params:
  colors:
    primary: "#6A0DAD"      # Your brand color
    secondary: "#00D4FF"
    accent: "#D6B656"
```

### Change Navigation

Edit `config.yaml`:
```yaml
menu:
  main:
    - name: "New Link"
      url: "/new-page/"
      weight: 25
```

---

## Testing Domain Routing Locally

Netlify redirects only work in production. To test locally, visit sections directly:
- http://localhost:1313/deia/
- http://localhost:1313/simdecisions/
- http://localhost:1313/efemera/

---

## Deployment Checklist

- [ ] Hugo installed
- [ ] Site builds locally (`hugo`)
- [ ] Netlify account created
- [ ] Repo connected to Netlify
- [ ] All 5 domains added to Netlify
- [ ] DNS updated at registrar
- [ ] SSL certificates provisioned
- [ ] Test all domain routes

---

## Troubleshooting

### Build fails on Netlify
- Check Hugo version in `netlify.toml`
- Verify build command: `cd website && hugo --minify`
- Check Hugo error logs in Netlify deploy log

### Domain not routing correctly
- Verify redirect in `netlify.toml`
- Check DNS propagation: https://dnschecker.org
- Try incognito/private browser (clear cache)

### SSL not working
- Wait 24 hours for DNS propagation
- Check domain is added in Netlify
- Verify nameservers updated at registrar

---

## Support

- GitHub: https://github.com/deiasolutions
- Docs: https://q33n.com/docs/
- Email: hello@q33n.com

---

*Built with Hugo • Hosted on Netlify • Powered by Q33N*
