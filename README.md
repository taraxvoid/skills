# claude-skills

Tara's skillz which won't ever pay the billz (but do important things anyway)

## Install

```
/plugin marketplace add taraxvoid/claude-skills
/plugin install trans-rights@taraxvoid-skills
/plugin install trans-wrongs@taraxvoid-skills
```

## Skills

- **trans-rights** — interviews you once for your chosen
  name/pronouns, then writes a directive into global `~/.claude/CLAUDE.md`
  so Claude stops treating `git config`, account name(s), and
  email addy as evidence of identity, and asks before writing your name/pronouns
  into anything potentially dayjob-facing (README, CLAUDE.md, PR/commit text, comments).
- **trans-wrongs** — flags forms/copy that force a binary/assumed gender,
  ask about sexuality gratuitously, assume a relationship structure, or
  collect a legal-only name with no display-name option. Runs either as a
  one-time full-repo audit (a standalone report) or as part of a PR/diff-time
  code review.

## Adding a new skill

1. `skills/<name>/SKILL.md` (+ optional `.claude-plugin/plugin.json` if it
   should be independently installable/versioned).
2. Add an entry to `.claude-plugin/marketplace.json` under `plugins`.
3. Commit, push to `main`.

## Local validation

A pre-commit hook validates repo integrity before every commit. It checks:

- **JSON validity** — all `.json` files parse without error
- **marketplace.json schema** — required top-level fields present
- **plugin.json schemas** — each plugin.json has name, version, description
- **Cross-reference integrity** — marketplace.json ↔ `skills/<name>/` ↔
  `SKILL.md` ↔ `plugin.json` (names match, no orphans)
- **Frontmatter** — `SKILL.md` has valid YAML frontmatter with a `name`
  matching its directory
- **Markdown hygiene** — no trailing whitespace, files end with newline

### Enable hooks (one-time per clone)

```bash
git config core.hooksPath hooks
```

### Run validation manually

```bash
python3 scripts/validate-skills.py
```

### Bypass the hook for a single commit

```bash
git commit --no-verify
```
