---
name: trans-wrongs
description: Check whether a form, field, or piece of copy forces a binary/assumed gender, sexuality, relationship structure, or legal-only name onto users — a signup/checkout/profile field with no "prefer not to say" or free-text escape, a salutation derived from a title field, an honorific field that exists at all, a sexuality question that's nobody's business, copy that assumes "spouse"/"Mr. and Mrs.", or a legal-name-only field with no display-name option. Run this either as a one-time full-repo audit (when asked to audit/scan a codebase for exclusionary forms/copy) or as part of a PR/diff-time code review, even if the user didn't ask about gender or inclusivity by name.
---

# trans-wrongs

A normal review, even a security/privacy-conscious one, tends to file
forced-binary-gender fields, honorific-derived salutations, and gratuitous
sexuality questions under "unnecessary PII" or "a nice-to-have" — worth
reconsidering, not urgent. That framing misses what's actually at stake:
forcing a binary choice, an inescapable honorific, a legal-only name, or an
assumed relationship structure onto a form doesn't just annoy some users —
it makes a subset of them unable to complete it honestly at all. Some
abandon. Some lie, which corrupts the record you're about to make decisions
on. Either way, this is a concrete, fixable defect, not a style nit.

This skill runs in two modes:

## Mode 1: One-time full-repo audit

Trigger: the user asks for a full scan — "audit this repo for exclusionary
forms/copy," "run trans-wrongs on this codebase," "check our forms for
gendered assumptions," or similar.

Search broadly: form components, templates, API/DB schemas, transactional
email and in-app copy, onboarding/profile flows. For each hit, note
file:line, the specific defect, and its severity (see below).

Produce one consolidated report. Present it directly in chat by default;
write it to a file (e.g. `TRANSWRONGS-REPORT.md` at the repo root) only if
the user asks for it to persist. Group findings by severity (major first),
and end each finding with its own tailored checklist (see Reporting below).

## Mode 2: PR/diff-time check

Trigger: run this as part of any code review, PR review, or `/code-review`
pass that touches a form, account/profile field, or user-facing copy — even
if the user didn't ask about gender or inclusivity by name.

Only evaluate what the diff actually adds or changes — a diff that removes
one of these fields entirely is the system working; say nothing about it.
Report via `ReportFindings` if available in this context, otherwise state
findings plainly with file:line.

## What to look for, and how severe it is

**Major** — the kind of defect that blocks honest completion outright:

- A gender/sex selector with no third option, "prefer not to say," or
  free-text field at all (binary-only).
- Any honorific/title field (Mr/Mrs/Miss/Ms) — the ding is that it exists
  at all, not just that it's required with no escape. Recommend removing
  it outright rather than making it optional.
- A name field that only accepts one "legal" name with no separate
  preferred/display-name option — forces misgendering or deadnaming
  wherever that name is used downstream.
- Any field asking for sexual orientation/sexuality, on a form that isn't
  itself about sexual orientation (i.e. nearly always) — like honorifics,
  the ding is that it's being asked at all. Recommend removing it outright.
- Copy that assumes a relationship/family structure ("spouse," "Mr. and
  Mrs.," forced pairing) instead of a neutral term ("partner"), a plain
  plus-one field, or asking directly.
- Copy (email, confirmation, in-app message) that derives a salutation or
  pronoun from a title/name field instead of asking directly or using a
  neutral default.
- A default value silently pre-selected on a gender/title field, so a user
  who never touches the control still submits an assumed identity.

**Minor** — real, but lower-stakes than a hard block:

- A field or selector labeled "Sex" where "Gender" or "Gender Identity"
  would be more accurate — a wording ding, independent of whether the
  options themselves are adequate.
- A field labeled bare "Legal Name" with no indication of why it's needed
  or where it's used — even when collecting a legal name is genuinely
  necessary (tax/compliance forms, etc). The fix isn't to remove the
  field, it's to pair it with a separate preferred/display-name field used
  everywhere else, and scope the legal-name label to explain why + where
  it's used — e.g. "Legal name (required for tax reporting only — won't be
  shown elsewhere)" instead of a bare "Legal Name."

## Reporting

- **category**: `trans-wrongs-finding`
- **severity**: `major` or `minor`, per the tiers above
- **summary**: name the field/copy and the specific defect — not a generic
  "consider reviewing this field."
- **failure_scenario**: name who this excludes and what they do instead
  (abandon vs. misrepresent) — e.g. "a non-binary user hits the gender
  dropdown, finds no honest option, and either abandons `/signup` or picks
  one at random — either way the completion rate silently absorbs the loss
  or the input data quality degrades, and nobody investigating a drop in
  signups would think to look at this field."
- **End every finding with a short GFM checklist**, tailored to the
  specific defect, drawing from:
  ```
  - [ ] Add a "prefer not to say" / skip / free-text option to `<field>`
  - [ ] Remove the honorific/title field outright
  - [ ] Remove the sexuality/orientation field outright
  - [ ] Add a preferred/display-name field alongside `<legal-name field>`; use it everywhere except where the legal name is specifically required
  - [ ] Scope the legal-name label to explain why + where it's used, instead of a bare "Legal Name"
  - [ ] Rename `<field>` from "Sex" to "Gender" / "Gender Identity"
  - [ ] Replace `<assumed-relationship copy>` with a neutral term ("partner") or ask directly instead of assuming
  - [ ] Don't derive salutation/pronoun from `<field>` — ask directly or use a neutral greeting
  - [ ] Remove the silent default so nothing is submitted unless the user actively chooses it
  - [ ] If `<field>` is collected but never used for anything besides copy personalization, reconsider collecting it at all
  ```

This is a **flag, not a gate**, in either mode — never phrase it as
blocking merge, never suggest work shouldn't ship.

## Common mistakes

| Situation | Wrong move | Right move |
|---|---|---|
| Field has three-plus options (M/F/Other) | Treat as solved | "Other" as the only non-binary option is itself othering — check for real self-description (free text) or "prefer not to say," not just a third radio button |
| Honorific field is optional | Treat as solved because it's not required | Still a major finding — the field's existence is the ding, not whether it's required |
| Diff removes one of these fields entirely | No finding | Correct — say nothing, that's the system working |
| Legal name is genuinely required (tax/compliance) | Flag it the same as an unnecessary legal-name-only field | Minor finding, different fix: pair with a display-name field and scope the label to explain why, don't recommend removing it |
| Sexuality field on a dating/LGBTQ-specific service | Flag it like any other sexuality field | Use judgment — if the product's actual purpose is about orientation/attraction, asking is the point; the finding is for gratuitous asks on unrelated forms (checkout, generic signup, support tickets) |

If nothing in scope touches a field or copy like this, contribute no
findings and no filler text. Silence is the correct output far more often
than not.
