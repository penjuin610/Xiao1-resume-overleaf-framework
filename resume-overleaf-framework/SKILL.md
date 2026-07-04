---
name: resume-overleaf-framework
description: Use when a user wants a JD-to-resume skill that updates a private Overleaf project through a user-controlled browser session. This skill is for the Overleaf workflow only; use the local LaTeX skill when the user wants local .tex files and latexmk builds.
---

# Resume Overleaf Framework

## Purpose

This skill controls the Overleaf version of a private JD-to-resume workflow.

It tells an AI agent how to:

1. read a JD
2. load private resume context
3. tailor a fixed LaTeX resume
4. update a private Overleaf project
5. compile in Overleaf
6. download and rename the final PDF

This skill is public-safe. It must not contain real personal data, private URLs, browser sessions, or machine-specific paths.

## Required Private Files

Before acting, load three private local files:

1. `facts-and-preferences.md`  
   Editing rules, page-fit rules, inclusion rules, and strategy preferences.

2. `resume-facts.md`  
   Factual resume database and hard truth constraints.

3. `private-config.md`  
   Overleaf project URL, naming rules, browser assumptions, and export notes.

If those files do not exist yet, stop and tell the user to create them from the templates in `references/`.

## What This Skill Must Never Do

- never invent experience
- never change dates, titles, employers, or locations unless the private files explicitly allow it
- never publish personal data into the public repo
- never assume a public skill can control a specific person's browser
- never hardcode private Overleaf URLs, credentials, or machine-specific access details

## Workflow

### 1. Read the JD

- accept a public JD link, company job page, or user-provided JD text
- identify the correct role before tailoring
- ask for clarification when the page contains multiple roles or too little information

### 2. Load Private Context

Read private files in this order:

1. `facts-and-preferences.md`
2. `resume-facts.md`
3. `private-config.md`

Understand:

- what must stay true
- what should usually be kept
- what is optional
- how the resume should be compressed or expanded
- how the final PDF should be named

### 3. Tailor The Resume

- preserve facts exactly
- map the JD to relevant experiences, projects, tools, and credentials
- keep the fixed LaTeX structure unless private instructions say otherwise
- remove low-priority experience before weakening core evidence
- avoid sparse one-page outputs and avoid tiny spillover onto a second page

### 4. Update Overleaf

- use only the private Overleaf project configured by the user
- prefer an already-authenticated browser session when available
- replace the LaTeX content
- recompile
- inspect compile status and page count

If login is expired or browser automation is blocked, pause and explain the exact blocker.

### 5. Export

- download the PDF
- rename it using the private naming rule
- store it in the configured output location
- report major trimming or selection choices

## Output Expectation

End with:

- modified files or source location
- final PDF path
- compile/export status
- whether the result met the page target
- concise note on the main tailoring choices

