# DEIA Quick Start

**Get auto-logging working in 3 minutes**

---

## Step 1: Install DEIA

```bash
git clone https://github.com/deiasolutions/deia.git
cd deia
pip install -e .
deia install
```

---

## Step 2: Set Up Claude Code Memory (One Time)

In Claude Code, type:

```
# deia-user
```

Claude will confirm: "Memory set!"

**That's it.** This only needs to be done once, ever.

---

## Step 3: Enable DEIA in Your Project

```bash
cd /path/to/your/project
deia init
```

DEIA will ask a few setup questions and create `.deia/` directory.

---

## Step 4: Start Using Claude Code

Open your project in Claude Code. Auto-logging is now enabled.

**What happens automatically:**
- Claude reads your project context on startup
- Logs conversations after major tasks
- Saves to `.deia/sessions/`
- Never lose context again

---

## That's It

**Three commands. One memory setup. Done.**

No configuration files to edit.
No complex setup.
Just works.

---

## Verify It's Working

After working with Claude for a bit, check:

```bash
ls .deia/sessions/
```

You should see conversation logs.

---

## Disable Auto-Logging (Optional)

If you want to turn it off:

```bash
deia config auto_log false
```

Turn it back on:

```bash
deia config auto_log true
```

---

## Need Help?

- [Full Documentation](README.md)
- [GitHub Issues](https://github.com/deiasolutions/deia/issues)
- [Memory Setup Details](DEIA_MEMORY_SETUP.md) (advanced)

**But honestly, you probably don't need any of that. It just works.**
