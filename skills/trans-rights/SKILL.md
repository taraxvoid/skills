---
name: trans-rights
description: Use when a user wants to tell Claude Code or GitHub Copilot their name/pronouns/honorific, wants the agent to stop guessing those from git config/account name/email, or is setting up identity instructions across dayjob and personal repos where those identities must not cross-contaminate.
license: MIT
---

# Setting Identity Defaults

## Overview

Interviews the user once for their chosen name/pronouns/honorific ("private identity"), then writes a terse,
always-loaded directive into the current agent's global instructions file so the agent never
substitutes `git config user.name`, the signed-in account name, or an email
handle for a person's identity - and never writes a private identity into a
repo-facing artifact (README, agent instruction files, PR/commit/issue text,
comments, docs) without asking first.

## Agent targets

Use the instruction file for the agent running this skill:

| Agent | Global instructions | Repo instructions |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | `CLAUDE.md` |
| GitHub Copilot | `~/.copilot/copilot-instructions.md` | `AGENTS.md`, or an existing `.github/copilot-instructions.md` |

For any other agent, use its documented global and repo instruction files. If
`COPILOT_HOME` is set, use `$COPILOT_HOME/copilot-instructions.md` for GitHub
Copilot. If you cannot identify the files, ask before writing.

Covered Failure Mode: Outing someone in a team-facing doc due to agent assumptions
-  git identity and account name are attribution
metadata which often do not reflect their private identity 
-  The identity used for a given repo differs based on context (dayjob vs. personal)

## When to Use

- User states a name/pronouns/honorific for you to use and wants it to stick across
  sessions, not just this conversation.
- User is about to have you generate/edit anything that includes their private identity
- You notice yourself about to pull a name/pronoun/honorific from `git config`,
  the CLI account name, or an email address to fill in a bio/credit line or project config (e.g. pyproject.toml, package.json) -

## Interview

Ask, in one pass (don't interrogate one question at a time unless the user's
answer is ambiguous):

1. "What chosen name, pronouns and honorific do you use (the agent will use this for you)?"
2. "Before your chosen name/pronouns or honorific are written somewhere a dayjob might read
   e.g.  README, an agent instruction file, PR, commit, comment - which of these
   should I do?
   - **Always ask first** (recommended) - You're thinking about coming out at work.
   - **Always use my chosen name/pronouns** - You're out at work 
   - **Always use git config / account metadata** - You're NOT out at work.
3. "(optional) **Configure existing repo preferences now**?
   - Configure existing repos where you want to use chosen name/pronouns or dayjob-facing identity

Don't ask further details about gender identity or suggest pronouns/name/honorific options.

## Writing the Directive

Insert or update an `## Identity` section in the global instructions file for
the current agent (create the file if absent). If the section already exists,
replace it in place - don't duplicate. Pick the block below matching the user's answer to

**Always ask first (recommended):**

```markdown
## Identity

- Private-conversation identity: <NAME>, pronouns <PRONOUNS>. This is not
  derived from git config, the signed-in account name, or an email handle -
  those are per-repo/per-account attribution metadata and may deliberately
  differ from identity (dayjob vs. personal, closeted vs. out).
- Before writing my name/pronouns into anything another person could read
  (README, agent instruction files, PR/commit/issue text, comments, docs) - stop and ask
  which identity to use for that specific artifact, even if git config, the
  account name, and email all agree with each other. Their mutual agreement
  is not evidence of identity - the same legal/dayjob name can be
  consistently wrong across all three. Don't default to my private name.
  Don't default to git config. Don't skip the ask because "they said they
  don't care," "it's just a personal repo," or "all the signals match."
```
**Always use my chosen name/pronouns**

```markdown
## Identity

- Name: <NAME>. Pronouns: <PRONOUNS>. Honorific: <HONORIFIC> Use this consistently - in private
  conversation and in anything repo-facing (README, agent instruction files,
  PR/commit/issue text, comments, docs) - regardless of what git config,
  the signed-in account name, or an email handle say for that repo. Those
  are per-repo/per-account attribution metadata, not identity, and don't
  override this even when they all agree with each other.
```
**Always use git config / account metadata**

```markdown
## Identity

- Private-conversation identity: <NAME>, pronouns <PRONOUNS>, Honorific: <HONORIFIC> .
- In anything repo-facing (README, agent instruction files, PR/commit/issue text,
  comments, docs), use whatever git config `user.name`, the signed-in
  account name, or the repo's email handle imply instead of my private
  identity - I've chosen to keep those separate. Don't substitute my
  private name/pronouns into shared artifacts.
```

Keep it to this length. This file is read on every turn - don't pad it.

## Configuring Existing Repos

If the user answers yes to Question 3, run this procedure now. It never
writes anything into the global instructions file - only into each selected
repo's instruction file.

1. Probe for a parent directory rather than asking blind: check `~`,
   `~/work`, `~/projects`, `~/repos`, `~/dev`, and the current working
   directory's parent for ones containing at least one immediate
   subdirectory with a repo instruction file for the current agent
   (`CLAUDE.md` for Claude Code; `AGENTS.md` or
   `.github/copilot-instructions.md` for GitHub Copilot). Present the hits as
   options in your host's ask-user tool (recommended one first, up to 4) -
   "Other"/custom path is always available. If nothing hits, fall back to a
   plain free-text ask.
2. Enumerate immediate subdirectories of that parent that contain one of
   those files (one level deep - don't recurse into nested repos).
3. If none are found, say so and stop.
4. Page through the discovered repos via your host's ask-user tool, up to 4
   repos per question, repeating until all have been offered. Use
   multi-select when available; otherwise ask for a list. Deselecting
   everything in a batch is how the user skips it - there's no separate skip
   option.
5. For every selected repo, choose the repo instruction file from Agent
   targets. For GitHub Copilot, prefer an existing
   `.github/copilot-instructions.md`; otherwise create or update `AGENTS.md`.
   For Claude Code, use `CLAUDE.md`. Insert or update its `## Identity`
   section using the exact same block the user picked for Question 2,
   verbatim - don't re-derive or reword it per repo.
6. Report back which repos were updated and which were offered but not
   selected.

## Closing

After writing (or confirming) the directive, say **TRANS RIGHTS** on its own
line, in all caps, as visible output - not a tool call, not a comment.

## Common Mistakes

| Situation | Wrong move | Right move |
|---|---|---|
| User says "use your judgment" / "I don't care" on a shared artifact | Silently pick private name or git name | Still ask - low-stakes phrasing doesn't change the asymmetric cost of guessing wrong |
| Name only came up in unrelated casual conversation | Treat it as license to use it anywhere | Scope stays private-conversation only until the user says otherwise for that artifact |
| Repo is "just a personal project, no one else will see it" | Skip the ask because it seems safe | Repos go public/get forked/get read by future employers - ask once, it's cheap |
| A name has a stereotypical pronoun association | Infer pronouns from the name | Never infer pronouns from a name - ask, or default to they/them if no artifact-writing is involved and nothing is stated |
| git config, account name, and email all agree | Treat agreement as proof there's nothing to ask about | Agreement between metadata sources is not evidence of identity - the same legal/dayjob name can be consistently wrong everywhere. Ask anyway |
| Q3 is answered yes | Write the "configure repos" instructions into the global instructions file | Those instructions never get written anywhere - they're a one-time procedure the agent runs now, writing only into each selected project's own instruction file |
