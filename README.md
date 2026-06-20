# Xiao1 Resume Overleaf Framework

This repository is the public-safe version of a private resume workflow.

It is designed for one job-search pattern:

1. read a JD from a public or logged-in page
2. map that JD to a private resume fact base
3. rewrite a fixed LaTeX resume
4. update a private Overleaf project
5. compile and download a job-specific PDF
6. save a local record of that application

This repository publishes the framework only.

It does not publish:

- any real name, email, phone number, city, or work history
- any private Overleaf URL
- any browser session or login state
- any private resume bullets or personal strategy notes
- any machine-specific path that would let someone control another person's computer

## What This Repo Is

- a public skill package that can be shown to any AI agent
- a safe explanation of how the workflow is structured
- a starter template for building a private resume engine on top of it

## What This Repo Is Not

- a plug-and-play repo that can tailor resumes without private input
- a personal resume database
- an auto-login or auto-control package for someone else's browser
- a finished hosted job-application product

## Repo Layout

```text
public-skill-package/
├── README.md
├── LOCAL_SETUP.md
├── OPTIONAL_EXTENSIONS.md
├── LICENSE
└── resume-overleaf-framework/
    ├── SKILL.md
    └── references/
        ├── facts-and-preferences-template.md
        ├── private-config-template.md
        └── resume-facts-template.md
```

## The 3 Private Files

A real deployment of this framework should have 3 private local documents.

1. `facts-and-preferences.md`
Purpose:
Stores strategy rules and editing preferences.
Examples:
what experiences are always kept, what can be removed, preferred page length, how to handle projects, how to compress for one page, writing style preferences.

2. `resume-facts.md`
Purpose:
Stores the factual resume database.
Examples:
name, contact info, education, job titles, dates, locations, safe themes, project links, hard truth constraints.

3. `private-config.md`
Purpose:
Stores local execution settings.
Examples:
Overleaf project URL, PDF naming rule, browser assumptions, login-handling notes, export behavior.

These files are intentionally not included with real values.

## How An AI Agent Should Use This Repo

Any AI agent using this framework should follow this order:

1. read `resume-overleaf-framework/SKILL.md`
2. read the user's private `facts-and-preferences.md`
3. read the user's private `resume-facts.md`
4. read the user's private `private-config.md`
5. read the JD
6. tailor the resume without changing facts
7. update Overleaf or another private LaTeX target
8. export and rename the final PDF

The public skill should never be treated as the source of truth by itself.
It is a controller, not the data layer.

## Quick Start

1. Clone or download this repository.
2. Create your own 3 private files from the templates in `resume-overleaf-framework/references/`.
3. Store those filled private files outside Git or under a Git-ignored private folder.
4. Install `resume-overleaf-framework/SKILL.md` into your local AI-agent skills folder.
5. Tell your agent where your private files live.
6. Test with one JD link before trying any automation.

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for a concrete local setup pattern.

## Privacy Model

Recommended split:

- public repo:
  framework, docs, templates, safe workflow logic
- private local overlay or private repo:
  actual resume database, exact preferences, Overleaf target, local paths, browser behavior

If a file contains personal resume content or live access details, keep it private.

## Optional Add-Ons

This repo can be extended, but those extensions are optional rather than required:

- local website shell with URL input and ledger history
- job ledger and run-history storage
- browser automation adapters
- local PDF fallback pipeline
- manual-review checkpoints before apply/submit

See [OPTIONAL_EXTENSIONS.md](OPTIONAL_EXTENSIONS.md).

## Audience

This repo is useful if you want:

- a reusable AI skill for JD-to-resume work
- a public-safe GitHub repo that explains your process
- a way to separate framework from personal data cleanly

## License

MIT. See [LICENSE](LICENSE).
