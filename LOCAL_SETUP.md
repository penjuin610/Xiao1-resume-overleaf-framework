# Local Setup

This repository is intentionally incomplete until the user adds private local files.

The public repo provides the framework.
The private overlay provides the real resume data.

## Goal

After setup, an AI agent should be able to:

1. read a JD link
2. load your private resume rules and facts
3. tailor the resume
4. update your private Overleaf project
5. export a renamed PDF

## Recommended Local Structure

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

## What Each Private File Does

### `facts-and-preferences.md`

Use this file for editing strategy.

Put here:

- which experiences are always retained
- which experiences are optional
- how projects should be used
- one-page vs 1.5-page vs 2-page rules
- compression preferences
- wording and tone preferences

### `resume-facts.md`

Use this file for factual data only.

Put here:

- your name and contact details
- education facts
- work experience facts
- project facts
- tools
- credentials
- hard truth rules such as dates and titles that must never change

### `private-config.md`

Use this file for local execution settings.

Put here:

- your Overleaf project URL
- your PDF naming convention
- your preferred browser workflow
- what the agent should do if login is expired
- any local notes for export behavior

## Install Into A Local Skill Folder

Different AI agents expose skills differently, but the general pattern is:

1. copy `resume-overleaf-framework/` into the agent's local skills directory
2. keep the 3 filled private files outside the public repo or inside a Git-ignored private folder
3. tell the agent to read the public skill and then your private files before acting

## Minimum Test

Before using the workflow for real applications:

1. open a JD link
2. ask the agent to explain which private files it will load
3. ask it to generate resume LaTeX only
4. verify that no facts were changed
5. only then test Overleaf update and PDF export

## Safety Rules

Never commit these into a public repo:

- filled private templates
- real Overleaf links
- browser/session assumptions that are tied to your machine
- any private resume bullets
- downloaded PDFs

## If You Want A Website Shell

The website shell is optional.
This repo does not require a frontend.

If you want a website later, use this repo as the logic layer and add:

- JD URL input
- run history / ledger
- run detail view
- download button
- optional browser automation trigger

See [OPTIONAL_EXTENSIONS.md](OPTIONAL_EXTENSIONS.md).
