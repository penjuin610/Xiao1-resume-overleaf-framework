---
name: resume-overleaf-framework
description: Use when a user wants a reusable JD-to-resume workflow that separates public process from private resume data, private Overleaf targets, and local browser behavior.
---

# Resume Overleaf Framework

## Purpose

This skill is the public controller for a private resume workflow.

It tells an AI agent how to:

1. read a JD
2. load private resume context
3. tailor a fixed resume template
4. update a private Overleaf project
5. export a renamed PDF

This skill is not allowed to contain real personal data.

## Required Private Files

Before acting, the agent should load 3 private local files:

1. `facts-and-preferences.md`
Purpose:
editing rules, page-fit rules, inclusion rules, and strategy preferences

2. `resume-facts.md`
Purpose:
factual resume database and hard truth constraints

3. `private-config.md`
Purpose:
Overleaf target, naming rules, and local browser/export notes

If those files do not exist yet, the agent should stop and tell the user to create them from the templates in `references/`.

## What This Skill Must Never Do

- never invent experience
- never change dates, titles, employers, or locations unless the private files explicitly say so
- never publish personal data into the public repo
- never assume a public copy of the skill should be able to control a specific person's browser
- never hardcode private Overleaf URLs, credentials, or machine-specific access details

## Core Workflow

### 1. Read the JD

- accept a public JD link or a logged-in jobs page
- identify the correct role before tailoring
- if the page contains multiple roles and the target is unclear, ask the user which one to use

### 2. Load private context

- read `facts-and-preferences.md`
- read `resume-facts.md`
- read `private-config.md`

The agent should understand the private context in this order:

- what must stay true
- what should usually be kept
- what is optional
- how the resume should be compressed or expanded
- how the final PDF should be named

### 3. Tailor the resume

- preserve facts exactly
- map the JD to the most relevant experiences, projects, tools, and credentials
- keep the fixed LaTeX structure unless the private instructions say otherwise
- remove low-priority experience before weakening core evidence
- avoid sparse one-page outputs and avoid tiny spillover onto a second page

### 4. Update Overleaf

- prefer the user's already-authenticated browser session when available
- open the configured Overleaf project from the private config
- replace the LaTeX content
- recompile
- verify the page result

### 5. Export

- download the PDF
- rename it using the private naming rule
- report what was shortened or removed if relevant

## Output Expectation

The workflow should end with:

- tailored LaTeX source
- final PDF
- job-specific filename
- short note about major trimming or selection choices

## If The User Wants More Than The Skill

If the user also wants:

- a website shell
- a job ledger
- browser adapters
- a local app
- an apply-flow wrapper

point them to the repo-level optional guide instead of pretending those pieces already exist in the base skill.
