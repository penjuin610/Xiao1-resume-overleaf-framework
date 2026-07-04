---
name: resume-local-latex-framework
description: Use when a user wants a JD-to-resume skill that edits local LaTeX files and compiles PDFs with a local TeX engine such as MacTeX or TeX Live. Use this instead of the Overleaf skill when the user asks for local .tex files, latexmk, XeLaTeX, TeXShop, or direct local PDF output.
---

# Resume Local LaTeX Framework

## Purpose

This skill controls the local LaTeX version of a private JD-to-resume workflow.

It tells an AI agent how to:

1. read a JD
2. extract a short JD signal file
3. create a role-specific workspace
4. load a compact private context package
5. tailor local `.tex` override files
6. compile with `latexmk`
7. validate the PDF
8. save the final PDF to a configured output folder

This skill is public-safe. It must not contain real personal data, private paths, or machine-specific secrets.

## Required Private Files

Before editing resume content, load:

1. `resume-facts.md`  
   Factual resume database and hard truth constraints.

2. `facts-and-preferences.md`  
   Editing strategy, page-fit rules, inclusion rules, and tone.

3. `local-config.md`  
   Resume engine path, compiler, output folder, build folder, and naming rules.

Optional but recommended for the local v2 workflow:

4. `private-profile.compact.json`  
   A compact machine-readable facts file used by `resume.py prepare-context` to select relevant factual anchors without loading the full private database every time.

If those files do not exist yet, stop and tell the user to create them from the templates in `references/`.

## Recommended Resume Engine Layout

```text
resume-engine/
├── source/
│   ├── main.tex
│   ├── preamble.tex
│   ├── content/
│   │   ├── profile.tex
│   │   ├── experience.tex
│   │   ├── projects.tex
│   │   ├── education.tex
│   │   └── skills.tex
│   └── roles/
│       └── [job-specific overrides]/
├── private/
│   ├── resume-facts.md
│   ├── facts-and-preferences.md
│   ├── private-profile.compact.json
│   └── local-config.md
├── output/
│   └── build/
├── resume.py
└── scripts/
    └── build_resume.sh
```

## What This Skill Must Never Do

- never invent experience
- never change dates, titles, employers, or locations unless private files explicitly allow it
- never paste private facts into a public repo
- never use Overleaf, browser automation, downloads, or login sessions
- never remove style or content just to hide a LaTeX error

## Workflow

### 1. Read And Compress The JD

- accept a public JD link, company job page, or user-provided JD text
- identify company, role, seniority, responsibilities, tools, industry keywords, and required skills
- save only the relevant JD signal into a short `jd.md`
- ask the user to paste/upload the JD if the page requires login, CAPTCHA, permission access, or cannot be reliably extracted
- do not repeatedly attempt browser automation for inaccessible pages

### 2. Initialize The Role

When `resume.py` is available, run:

```sh
python3 resume.py init-job --company "Company" --role "Role" --jd-file "/path/to/jd.md"
```

This should:

- create a safe role key
- create `source/roles/<role-key>/`
- copy `jd.md`
- write `job.json`
- update `source/roles/active.tex`
- avoid copying every baseline `.tex` file

### 3. Prepare Minimal Context

Run:

```sh
python3 resume.py prepare-context --role-key "<role-key>"
```

Then read only:

1. generated `source/roles/<role-key>/context.md`
2. baseline `.tex` sections recommended by the context
3. relevant raw fact paragraphs only when fact verification is needed

Understand:

- factual boundaries
- default and optional experiences
- safe claims
- forbidden claims
- preferred page target
- output naming rule

### 4. Edit Local LaTeX Files

Prefer small edits:

- create job-specific overrides under `source/roles/<role-key>/`
- edit only needed sections, usually `experience.tex`, `skills.tex`, and `projects.tex`

Avoid rewriting the whole resume when a local override is enough. Do not modify baseline content to fit a single JD.

### 5. Compile Locally

Use `resume.py build` when available. It must call the configured build script instead of reimplementing LaTeX logic.

Default command:

```sh
python3 resume.py build --company "Company" --role "Role" --require-one-page
```

Fallback command:

```sh
./scripts/build_resume.sh --company "Company" --role "Role" --require-one-page
```

Prefer XeLaTeX unless the template explicitly requires another engine.

If a package is missing, report the missing package clearly. Do not delete styling or resume content to bypass the error.

### 6. Validate The PDF

Check:

- PDF exists in the configured final output folder
- page count matches the target
- no LaTeX errors
- no missing font warnings
- no overfull or underfull layout warnings
- no blank pages
- text extracts without mojibake

Useful commands:

```sh
pdfinfo final.pdf
pdffonts final.pdf
pdftotext final.pdf -
```

### 7. Reset Baseline When Needed

After smoke tests or when returning the engine to its default state, run:

```sh
python3 resume.py reset-baseline
```

## Output Expectation

End with:

- modified files
- true experiences retained or emphasized
- content removed or compressed
- compile status
- full final PDF path
- whether the result met the page target
- any facts that need user confirmation
