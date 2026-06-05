---
name: resume-overleaf-framework
description: Use when a user wants to turn a job description into a tailored resume, update an Overleaf project, compile the PDF, and export a job-specific file while keeping personal data in a separate private configuration.
---

# Resume Overleaf Framework

## Overview

This is a reusable framework for a private resume-tailoring workflow.

It supports this high-level flow:

1. Read a job description from a public page or a logged-in jobs page
2. Map the JD to a private resume fact base
3. Rewrite the resume in a fixed LaTeX template
4. Update a private Overleaf project
5. Compile and export the final PDF
6. Rename the exported PDF using a job-specific filename

This public skill must never hardcode personal resume data, browser targets, or private project URLs.

## When To Use

Use this skill when the user:

- sends a JD link and wants a tailored resume
- asks to update a resume in Overleaf
- wants a repeatable browser-assisted resume workflow
- wants a framework that separates public process from private profile data

Do not use this skill as the sole source of resume truth. It requires a private local profile.

## Required Private Inputs

Before using this framework, load the user's own private files:

- personal fact base
- resume preferences
- Overleaf project target
- PDF naming convention
- browser workflow notes

Use the templates in `references/` as examples of what the user must create locally.

## Rules

- Keep public framework and private profile data separate.
- Never commit personal facts, emails, phone numbers, exact resume content, or private URLs into the public version of the skill.
- Never assume a downloaded public copy of the skill should be able to control a specific person's browser or computer.
- Treat Overleaf targets, local paths, and naming conventions as private configuration.

## Workflow

### 1. Read the JD

- Accept a public JD URL or a jobs page from a logged-in browser session.
- If the page contains multiple postings, identify the target role before proceeding.
- If the page is ambiguous, ask the user which role to use.

### 2. Load the private profile

- Read the user's private fact base and preferences from local-only files.
- Determine:
  - core experiences
  - optional experiences
  - education detail level
  - one-page vs multi-page preference
  - naming convention
  - private Overleaf target

### 3. Tailor the resume

- Preserve facts exactly.
- Tailor language to the JD.
- Keep the user's fixed LaTeX structure unless the private rules say otherwise.
- Cut low-priority experience before weakening core experience or distorting facts.

### 4. Update Overleaf

- Use the user's already-authenticated browser session when available.
- Open the user's configured Overleaf project.
- Replace the LaTeX content.
- Recompile and verify the page count.

### 5. Export and rename

- Download the compiled PDF.
- Rename it using the private naming rule.

## Output

The workflow should end with:

- updated LaTeX source
- compiled PDF
- renamed PDF file
- short note on what was shortened or removed, if relevant
