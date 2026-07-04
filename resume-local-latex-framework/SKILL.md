---
name: resume-local-latex-framework
description: Use when a user wants a JD-to-resume skill that edits local LaTeX files and compiles PDFs with a local TeX engine such as MacTeX or TeX Live. Use this instead of the Overleaf skill when the user asks for local .tex files, latexmk, XeLaTeX, TeXShop, or direct local PDF output.
---

# Resume Local LaTeX Framework

## Purpose

This skill controls the local LaTeX version of a private JD-to-resume workflow.

It tells an AI agent how to:

1. read a JD
2. load private resume context
3. tailor local `.tex` files
4. compile with `latexmk`
5. validate the PDF
6. save the final PDF to a configured output folder

This skill is public-safe. It must not contain real personal data, private paths, or machine-specific secrets.

## Required Private Files

Before editing resume content, load:

1. `resume-facts.md`  
   Factual resume database and hard truth constraints.

2. `facts-and-preferences.md`  
   Editing strategy, page-fit rules, inclusion rules, and tone.

3. `local-config.md`  
   Resume engine path, compiler, output folder, build folder, and naming rules.

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
│   └── local-config.md
├── output/
│   └── build/
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

### 1. Read The JD

- accept a public JD link, company job page, or user-provided JD text
- identify company, role, seniority, responsibilities, and required skills
- ask for clarification when the target role is ambiguous

### 2. Load Private Context

Read:

1. `resume-facts.md`
2. `facts-and-preferences.md`
3. `local-config.md`

Understand:

- factual boundaries
- default and optional experiences
- safe claims
- forbidden claims
- preferred page target
- output naming rule

### 3. Edit Local LaTeX Files

Prefer small edits:

- update only relevant `source/content/*.tex` modules, or
- create job-specific overrides under `source/roles/[company-role]/`

Avoid rewriting the whole resume when a module override is enough.

### 4. Compile Locally

Use `latexmk` through the configured build script.

Default command shape:

```sh
./scripts/build_resume.sh --company "Company" --role "Role" --require-one-page
```

Prefer XeLaTeX unless the template explicitly requires another engine.

If a package is missing, report the missing package clearly. Do not delete styling or resume content to bypass the error.

### 5. Validate The PDF

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

## Output Expectation

End with:

- modified files
- true experiences retained or emphasized
- content removed or compressed
- compile status
- full final PDF path
- whether the result met the page target

