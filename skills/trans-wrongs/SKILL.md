---
name: trans-wrongs
description: Check whether a form, field, or piece of copy forces a binary/assumed gender, sexuality, relationship structure (including poly exclusion), parental terms, age, or legal-only name onto users — a signup/checkout/profile field with no "prefer not to say" or free-text escape, a salutation derived from a title field, an honorific field that exists at all, a sexuality question that's nobody's business, copy that assumes "spouse"/"Mr. and Mrs."/"Mother's Name", an exact age/DOB field, or a legal-name-only field with no display-name option. Also flags good practice worth calling out (poly-inclusive options, an optional pronoun field on a signup form). Applies to forms AND non-form copy — error messages, notifications, marketing/onboarding copy, docs. Run this either as a one-time full-repo audit (when asked to audit/scan a codebase for exclusionary forms/copy) or as part of a PR/diff-time code review, even if the user didn't ask about gender or inclusivity by name.
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

Search broadly, and don't stop at forms. Cover: form components, templates,
API/DB schemas, transactional email, onboarding/profile flows, error/toast
messages, push and in-app notifications, marketing and onboarding copy, and
docs. A gendered assumption in a push notification or a support-ticket
autoresponder is just as much a finding as one in a signup form. For each
hit, note file:line, the specific defect, and its severity (see below).

Produce one consolidated report. Present it directly in chat by default;
write it to a file (e.g. `TRANSWRONGS-REPORT.md` at the repo root) only if
the user asks for it to persist. Group findings by severity (violations
first), and end each finding with its own tailored checklist (see Reporting
below).

## Mode 2: PR/diff-time check

Trigger: run this as part of any code review, PR review, or `/code-review`
pass that touches a form, account/profile field, or user-facing copy — even
if the user didn't ask about gender or inclusivity by name.

Only evaluate what the diff actually adds or changes — a diff that removes
one of these fields entirely is the system working; say nothing about it.
Report via `ReportFindings` if available in this context, otherwise state
findings plainly with file:line.

## Severity tiers

Three tiers: **Violation** (blocks honest completion outright), **Warning**
(real, but lower-stakes), and **Good** (worth calling out even though
nothing's wrong — see below). Never phrase a Violation or Warning as
blocking merge; this is a flag, not a gate, in either mode.

### Violation

- A gender/sex selector with no third option, "prefer not to say," or
  free-text field at all (binary-only).
- Any honorific/title field (Mr/Mrs/Miss/Ms) — the ding is that it exists
  at all, not just that it's required with no escape. Recommend removing
  it outright rather than making it optional.
- A name field that only accepts one "legal" name with no separate
  preferred/display-name option — forces misgendering or deadnaming
  wherever that name is used downstream.
- A display-name field that exists but is **not user-choosable at account
  creation and/or not editable after creation** — this is the case that
  lets a legal name/deadname leak through permanently even though a
  display-name concept nominally exists.
- Any field asking for sexual orientation/sexuality, on a form that isn't
  itself about sexual orientation (i.e. nearly always) — like honorifics,
  the ding is that it's being asked at all. Recommend removing it outright.
- Copy that assumes a relationship/family structure ("spouse," "Mr. and
  Mrs.," forced pairing) instead of a neutral term ("partner"), a plain
  plus-one field, or asking directly. Includes forced gendered-partner
  terms ("husband"/"wife") and forced pairing (only a single partner slot
  with no support for multiple partners where relevant).
- Forced gendered-parent-only terms (e.g. "Mother's Name"/"Father's Name")
  with no parent/guardian alternative.
- Copy (email, confirmation, in-app message) that derives a salutation or
  pronoun from a title/name field instead of asking directly or using a
  neutral default.
- A default value silently pre-selected on a gender/title field, so a user
  who never touches the control still submits an assumed identity.
- An exact age or date-of-birth field where only a legal-age threshold is
  actually needed (e.g. collecting a full DOB just to gate 19+/21+ access).

### Warning

- A field or selector labeled "Sex" where "Gender" or "Gender Identity"
  would be more accurate — a wording ding, independent of whether the
  options themselves are adequate. (Carve-out: see below for medical
  context.)
- A field labeled bare "Legal Name" with no indication of why it's needed
  or where it's used — even when collecting a legal name is genuinely
  necessary (tax/compliance forms, etc). The fix isn't to remove the
  field, it's to pair it with a separate preferred/display-name field used
  everywhere else, and scope the legal-name label to explain why + where
  it's used — e.g. "Legal name (required for tax reporting only — won't be
  shown elsewhere)" instead of a bare "Legal Name."
- **No display-name field at all** — the "missing" case, distinct from the
  Violation case above (an existing-but-uneditable display name).
- A relationship field limited to mono-normative options only
  ("Spouse"/"Partner" radio, no self-describe, no multi-partner support) —
  narrower than the Violation case (forced/gendered terms), but still
  excludes poly relationships.
- An age-range/bracket selector (e.g. "25–34") — narrower than needed, but
  not as bad as an exact DOB field.

### Good

Call out positive findings too, framed as commendation or a low-cost
suggestion — never as a defect. Two flavors:

- **Commend**: the copy/form already does something right — e.g. a
  relationship field offers free self-describe text or explicit
  non-monogamous/poly options, or a gender field has a genuine "prefer not
  to say"/self-describe option.
- **Suggest**: a low-cost addition would be good practice — e.g. a
  name-collecting marketing/newsletter/account-signup form has no optional
  pronoun field alongside name. Note it as an opportunity ("along with
  name, this would make the copy more personal and signal the product is
  trans-aware"), not a gap. Scope this suggestion to forms that are
  actually collecting a name for personalization (signup/newsletter/account
  creation) — don't suggest it on every form that happens to have a name
  field (e.g. checkout, support tickets).

## No-finding carve-outs

- A "Sex" field on a form that's clearly medical/clinical (health intake,
  insurance, clinical-trial signup) — no finding at all, not even the
  Sex-vs-Gender Warning. Outside a medical context, the normal binary-only
  and Sex-vs-Gender rules apply.
- A boolean "confirm you are over 19/21" legal-age-threshold checkbox — no
  finding, as long as it only gates on the threshold and doesn't collect
  the actual age or DOB. (An age-range selector or exact-age/DOB field is
  a different case — see Warning/Violation above.)
- A sexuality field on a dating/LGBTQ-specific service, where the product's
  actual purpose is about orientation/attraction.
- A diff that removes one of these fields entirely — the system working,
  say nothing.

## Reporting

- **category**: `trans-wrongs-finding`
- **severity**: `violation`, `warning`, or `good`, per the tiers above
- **summary**: name the field/copy and the specific defect (or, for Good,
  the specific positive practice or suggestion) — not a generic "consider
  reviewing this field."
- **failure_scenario** (Violation/Warning only): name who this excludes and
  what they do instead (abandon vs. misrepresent) — e.g. "a non-binary
  user hits the gender dropdown, finds no honest option, and either
  abandons `/signup` or picks one at random — either way the completion
  rate silently absorbs the loss or the input data quality degrades, and
  nobody investigating a drop in signups would think to look at this
  field."
- **why_it_helps** (Good only, replaces `failure_scenario`): name who
  benefits and how — e.g. "a poly user signing up sees their relationship
  structure isn't erased by the form, which is a small but real trust
  signal."
- **End every finding with a short GFM checklist**, tailored to the
  specific defect (Violation/Warning) or suggestion (Good), drawing from:
  ```
  - [ ] Add a "prefer not to say" / skip / free-text option to `<field>`
  - [ ] Remove the honorific/title field outright
  - [ ] Remove the sexuality/orientation field outright
  - [ ] Add a preferred/display-name field alongside `<legal-name field>`; use it everywhere except where the legal name is specifically required
  - [ ] Make the display name choosable at account creation and editable afterward, not just pre-filled from the legal name
  - [ ] Scope the legal-name label to explain why + where it's used, instead of a bare "Legal Name"
  - [ ] Rename `<field>` from "Sex" to "Gender" / "Gender Identity"
  - [ ] Replace `<assumed-relationship copy>` with a neutral term ("partner") or ask directly instead of assuming
  - [ ] Add a self-describe or explicit non-monogamous/poly option to `<relationship field>`
  - [ ] Add a parent/guardian alternative to `<gendered-parent-only field>`
  - [ ] Replace `<DOB/exact-age field>` with a legal-age-threshold confirmation instead of collecting the actual age
  - [ ] Don't derive salutation/pronoun from `<field>` — ask directly or use a neutral greeting
  - [ ] Remove the silent default so nothing is submitted unless the user actively chooses it
  - [ ] Consider adding an optional pronoun field alongside name on `<signup form>`
  - [ ] If `<field>` is collected but never used for anything besides copy personalization, reconsider collecting it at all
  ```

## Common mistakes

| Situation | Wrong move | Right move |
|---|---|---|
| Field has three-plus options (M/F/Other) | Treat as solved | "Other" as the only non-binary option is itself othering — check for real self-description (free text) or "prefer not to say," not just a third radio button |
| Honorific field is optional | Treat as solved because it's not required | Still a Violation — the field's existence is the ding, not whether it's required |
| Diff removes one of these fields entirely | No finding | Correct — say nothing, that's the system working |
| Legal name is genuinely required (tax/compliance) | Flag it the same as an unnecessary legal-name-only field | Warning, different fix: pair with a display-name field and scope the label to explain why, don't recommend removing it |
| Sexuality field on a dating/LGBTQ-specific service | Flag it like any other sexuality field | Use judgment — if the product's actual purpose is about orientation/attraction, asking is the point; the finding is for gratuitous asks on unrelated forms (checkout, generic signup, support tickets) |
| Relationship field offers only "Spouse"/"Partner", no self-describe | Treat as solved (not gendered) | Still a Warning — mono-normative framing excludes poly even without gendered terms |
| "Sex" field on a medical intake / insurance / clinical-trial form | Flag like any other Sex-vs-Gender wording issue | No finding — medical context is a legitimate carve-out |
| Display name field exists, pre-filled from legal name, user can edit it at signup | Treat as solved | Still check: is it editable *after* account creation too, not just at signup? |
| Age field is a yes/no "are you over 19/21" checkbox | Flag for asking about age | No finding — legal threshold gates are fine as long as they don't collect the actual age/DOB |

If nothing in scope touches a field or copy like this, contribute no
findings and no filler text. Silence is the correct output far more often
than not.
