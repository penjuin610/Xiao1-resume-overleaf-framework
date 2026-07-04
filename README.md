# Resume Workflow Skills

This repository is a public-safe skill package for AI-assisted JD-to-resume work.

It documents two ways to run the same core workflow:

1. **Overleaf browser workflow**: an agent updates a private Overleaf project through a user-controlled browser session, recompiles online, then exports the PDF.
2. **Local LaTeX workflow**: an agent edits local `.tex` files, compiles with a local TeX installation such as MacTeX, and writes the final PDF to a local output folder.

Both workflows use the same principle:

- the public repo stores process and templates
- the private overlay stores real resume facts, private paths, URLs, and preferences
- the agent must tailor only from confirmed facts

This repository intentionally contains no real personal resume data.

## Latest Update: Local Workflow v2

The previous version introduced the two workflow choices above: an Overleaf browser workflow for users who keep their canonical resume in Overleaf, and a local LaTeX workflow for users who prefer local `.tex` files and local PDF builds.

This update keeps that split, but makes the local workflow more efficient and more reproducible. The local path now includes a small `resume.py` helper that handles deterministic, repetitive steps:

- create a role folder and safe role key
- store a short `jd.md`
- generate a compact `context.md`
- activate a role by updating `source/roles/active.tex`
- call the existing `scripts/build_resume.sh`
- return short JSON instead of long LaTeX logs
- append a private application ledger
- reset back to baseline

The design goal is **not** to let Python write the resume. The agent still reads the JD, checks facts, and edits only the necessary LaTeX override files. Python simply removes mechanical work that would otherwise waste context tokens.

## What This Repo Does Not Include

- real name, email, phone number, city, or work history
- private Overleaf project URLs
- browser session data or login state
- private resume bullets or application strategy notes
- machine-specific paths that would control a real computer
- generated resume PDFs

## Repo Layout

```text
public-skill-package/
├── README.md
├── LOCAL_SETUP.md
├── OPTIONAL_EXTENSIONS.md
├── LICENSE
├── resume-overleaf-framework/
│   ├── SKILL.md
│   └── references/
│       ├── facts-and-preferences-template.md
│       ├── private-config-template.md
│       └── resume-facts-template.md
└── resume-local-latex-framework/
    ├── SKILL.md
    ├── references/
    │   ├── local-config-template.md
    │   ├── facts-and-preferences-template.md
    │   └── resume-facts-template.md
    └── scripts/
        ├── resume.py
        └── build_resume.sh
```

## Which Workflow Should I Use?

Use the **Overleaf browser workflow** when:

- your canonical resume template already lives in Overleaf
- you want Overleaf to compile and preview the PDF
- your AI agent can safely use an already-authenticated browser session
- you prefer a browser-based editing and export loop

Use the **local LaTeX workflow** when:

- you have MacTeX, TeX Live, or another local TeX distribution installed
- you want faster local builds without browser automation
- you want files organized as a local resume engine
- you want the final PDF written directly to a local output folder
- you want deterministic helper commands to reduce repeated context loading and long build logs

## Shared Private Files

A real deployment should create private local files from the templates.

1. `resume-facts.md`  
   Factual resume database: contact fields, education, titles, dates, employers, locations, projects, safe themes, tools, credentials, and hard truth rules.

2. `facts-and-preferences.md`  
   Editing strategy: default experiences, optional experiences, project placement, page-fit rules, compression preferences, tone, and forbidden claims.

3. Workflow config file  
   Use `private-config.md` for Overleaf, or `local-config.md` for local LaTeX. This file stores private execution details such as output paths, naming rules, and tool assumptions.

Filled versions should stay outside the public repo or inside a Git-ignored private directory.

## AI Agent Workflow

For either mode, the agent should:

1. read the relevant `SKILL.md`
2. read the private fact base and preferences
3. read the workflow config
4. read the JD
5. map the JD to real experiences, projects, tools, and credentials
6. edit the resume without inventing facts
7. compile/export the PDF through the selected workflow
8. validate page count, errors, warnings, and final filename

For the local v2 mode, the agent should use this shorter loop:

1. read the JD link or pasted JD text and save a short `jd.md`
2. run `python3 resume.py init-job`
3. run `python3 resume.py prepare-context`
4. read only `context.md` and the baseline sections that need overrides
5. edit only files under `source/roles/<role-key>/`
6. run `python3 resume.py build --company "..." --role "..." --require-one-page`
7. report the final PDF path, page count, changed override files, and any fact questions

## Safety Model

The public skill is a controller, not a data layer.

The agent must not:

- invent experience or dates
- inflate titles or project ownership
- copy private facts into this public repository
- hardcode private URLs, local paths, or credentials
- assume a public skill can control a specific browser or machine

## Quick Start

1. Clone this repository.
2. Pick one workflow: Overleaf or local LaTeX.
3. Copy the matching skill folder into your AI agent's local skills directory.
4. Create private files from the templates under that skill's `references/`.
5. Store filled private files outside Git or under a Git-ignored private folder.
6. Test with one JD link and review the generated resume before automating exports.

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for setup examples.

## Optional Add-Ons

The framework can be extended with:

- a local web app
- a run ledger
- browser adapters
- a local PDF build pipeline
- manual review checkpoints
- application-form assistance

See [OPTIONAL_EXTENSIONS.md](OPTIONAL_EXTENSIONS.md).

## License

MIT. See [LICENSE](LICENSE).
