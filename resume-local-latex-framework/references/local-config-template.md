# Local Config Template

Create a private local file from this template.
Do not commit the filled version to a public repository.

## Local Resume Engine

- Resume engine directory: `<absolute path to your private resume-engine>`
- LaTeX entrypoint: `<source/main.tex>`
- Build script: `<scripts/build_resume.sh>`
- Compiler: `<xelatex / pdflatex / lualatex>`

## Output

- Final PDF output folder: `<absolute path to final PDF folder>`
- Temporary build folder: `<absolute path to build artifact folder>`
- PDF filename format: `<Your_Name>_<Company>_<Role>.pdf`

Examples:

- `Jane_Doe_Stripe_Data_Analyst.pdf`
- `Jane_Doe_RBC_Risk_Analyst.pdf`

## Build Command

```sh
./scripts/build_resume.sh --company "<Company>" --role "<Role>" --require-one-page
```

## Validation Requirements

- compile must succeed
- PDF must exist in the final output folder
- page count must match the configured target
- log must not contain LaTeX errors
- log should not contain overfull/underfull warnings
- fonts should be embedded
- text should extract cleanly

