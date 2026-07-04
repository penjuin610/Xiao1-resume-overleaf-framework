# Local Setup

This repository is intentionally incomplete until you add private local files.

The public repo provides reusable skill logic. Your private overlay provides real resume data, execution paths, and workflow preferences.

## Setup Option A: Overleaf Browser Workflow

Use this option when your resume source lives in Overleaf and you want the agent to update a private Overleaf project.

Recommended structure:

```text
your-workspace/
├── public-skill-package/
│   └── resume-overleaf-framework/
│       ├── SKILL.md
│       └── references/
│           ├── facts-and-preferences-template.md
│           ├── private-config-template.md
│           └── resume-facts-template.md
└── private/
    └── resume-overleaf-framework/
        ├── facts-and-preferences.md
        ├── private-config.md
        └── resume-facts.md
```

`private-config.md` should contain:

- private Overleaf project URL
- PDF naming convention
- preferred browser workflow
- what to do if login expires
- whether to download automatically or pause for review

Minimum test:

1. Ask the agent to read a JD.
2. Ask it to explain which private files it will load.
3. Ask it to generate LaTeX only.
4. Review facts and page-fit decisions.
5. Only then test Overleaf update and PDF export.

## Setup Option B: Local LaTeX Workflow

Use this option when you want the agent to edit local `.tex` files and compile with a local TeX engine.

Recommended structure:

```text
your-workspace/
├── public-skill-package/
│   └── resume-local-latex-framework/
│       ├── SKILL.md
│       ├── references/
│       │   ├── facts-and-preferences-template.md
│       │   ├── local-config-template.md
│       │   └── resume-facts-template.md
│       └── scripts/
│           └── build_resume.sh
├── resume-engine/
│   ├── source/
│   │   ├── main.tex
│   │   ├── preamble.tex
│   │   ├── content/
│   │   └── roles/
│   ├── private/
│   │   ├── facts-and-preferences.md
│   │   ├── private-profile.compact.json
│   │   ├── local-config.md
│   │   └── resume-facts.md
│   ├── output/
│   │   └── build/
│   ├── resume.py
│   └── scripts/
│       └── build_resume.sh
└── resumes/
    └── 2026/
```

`local-config.md` should contain:

- local resume engine directory
- LaTeX entrypoint
- output folder for final PDFs
- build folder for temporary files
- compiler choice, usually XeLaTeX
- PDF naming convention

Minimum test:

```sh
./scripts/build_resume.sh --company "ExampleCo" --role "Analyst" --require-one-page
```

Then verify:

- PDF exists in the configured final output folder
- `pdfinfo` reports the expected page count
- build log has no LaTeX errors
- there are no missing font warnings
- text extracts without mojibake

### Optional Local v2 Helper

Copy `resume-local-latex-framework/scripts/resume.py` into your private `resume-engine/` root if you want the deterministic helper workflow.

Example flow:

```sh
cd /path/to/resume-engine

python3 resume.py init-job \
  --company "ExampleCo" \
  --role "Data Analyst" \
  --jd-file "/path/to/short-jd.md"

python3 resume.py prepare-context \
  --role-key "exampleco-data-analyst"

python3 resume.py build \
  --company "ExampleCo" \
  --role "Data Analyst" \
  --require-one-page

python3 resume.py reset-baseline
```

`resume.py` should not generate resume bullets or call an AI API. It only prepares folders, context, build commands, concise JSON output, and private ledger entries.

## What Each Private File Does

### `resume-facts.md`

Use this file for factual data only:

- name and contact placeholders
- education facts
- work experience facts
- project facts
- tools
- credentials
- hard truth rules such as dates and titles that must never change

### `facts-and-preferences.md`

Use this file for editing strategy:

- default experiences
- optional experiences
- project placement rules
- one-page or two-page preferences
- compression rules
- forbidden claims
- tone and wording preferences

### Workflow config

Use `private-config.md` for Overleaf or `local-config.md` for local LaTeX.

This file should store execution details, not resume facts.

## Install Into A Local Skill Folder

Different AI agents expose skills differently, but the general pattern is:

1. copy either `resume-overleaf-framework/` or `resume-local-latex-framework/` into the agent's local skills directory
2. keep filled private files outside the public repo or inside a Git-ignored private folder
3. tell the agent where those private files live
4. test with a non-sensitive JD before using the workflow for real applications

## Safety Rules

Never commit these into a public repo:

- filled private templates
- real Overleaf links
- real local paths
- browser/session assumptions tied to your machine
- private resume bullets
- downloaded PDFs
- generated role-specific `jd.md`, `context.md`, `job.json`, and application ledger files
- generated `.aux`, `.log`, `.out`, `.xdv`, or other build artifacts
