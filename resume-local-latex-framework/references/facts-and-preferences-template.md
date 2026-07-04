# Facts And Preferences Template

Create a private local strategy file from this template.
Do not commit the filled version to a public repository.

## Resume Strategy

- Default page target: `<one page / two pages / role-dependent>`
- Default experiences to keep:
  - `<experience>`
- Optional experiences:
  - `<experience>`
- Projects to use only when relevant:
  - `<project>`

## Tailoring Rules

- How to prioritize experiences for finance roles:
  - `<rule>`
- How to prioritize experiences for analytics roles:
  - `<rule>`
- How to handle AI or tooling projects:
  - `<rule>`

## Compression Rules

- First shorten:
  - `<section or bullet type>`
- Then remove:
  - `<lower-priority item>`
- Never remove without approval:
  - `<critical item>`

## Forbidden Claims

- Do not claim:
  - `<claim>`
- Do not overstate:
  - `<tool or skill>`

## Tone

- Preferred tone:
  - `<concise / analytical / client-facing / technical>`
- Avoid:
  - `<phrasing style>`

## Local Build Workflow

- JD input can come from a public link or pasted text.
- Extract only responsibilities, requirements, tools, industry keywords, and seniority.
- If the JD cannot be reliably extracted because of login, CAPTCHA, permissions, or page ambiguity, ask the user to paste/upload the JD.
- Do not use Overleaf for the local workflow.
- Do not use browser automation to compile, export, or download PDFs.
- Use `resume.py init-job` to create the role workspace and activate the role.
- Use `resume.py prepare-context` to create a compact context pack.
- Edit only necessary overrides under `source/roles/<role-key>/`.
- Use `resume.py build`, which wraps `scripts/build_resume.sh`, for local compilation.
- Use `resume.py reset-baseline` to restore the default baseline role.
