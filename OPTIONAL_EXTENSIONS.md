# Optional Extensions

These are optional build directions for people who want more than the base skill.

They are not required to use the framework.

## 1. Local Website Shell

Use this if you want a private app instead of typing every JD directly into a chat.

Suggested features:

- input box for JD URL
- `Generate Resume` button
- progress state
- local run history / ledger
- download button for the final PDF
- detail panel showing JD summary, salary, work mode, and role focus

## 2. Run Ledger

Use this if you want application history.

Suggested fields:

- date
- company
- role title
- source URL
- salary summary
- work mode
- employment type
- PDF filename
- JD summary
- key focus areas

## 3. Browser Automation Layer

Use this with the Overleaf workflow if you want an agent to control an already logged-in browser session.

Recommended scope:

- open the JD page
- extract the JD
- open the existing Overleaf project
- replace LaTeX source
- recompile
- download PDF

Do not design the public repo so that it can automatically control a stranger's machine.

## 4. Local LaTeX Build Layer

Use this with the local workflow, or as a fallback when Overleaf is unavailable.

Recommended scope:

- keep `.tex` source in a local resume engine
- compile with `latexmk`
- write temporary build files to a build folder
- copy only the final PDF to an output folder
- verify page count and warnings after each build

## 5. Manual Review Mode

Use this if you want an approval step before export.

Suggested review checkpoints:

- selected experiences
- selected projects
- chosen credentials
- page-length target
- final filename

## 6. Application-Form Assist

Use this only as a separate, clearly bounded module.

Suggested boundary:

- resume generation is one module
- application submission is another module

Do not auto-submit forms without explicit user approval.

## Recommendation

Start with this order:

1. public skill
2. private files
3. JD-to-resume generation
4. choose Overleaf export or local LaTeX build
5. ledger
6. website shell
7. form-assist or apply workflows
