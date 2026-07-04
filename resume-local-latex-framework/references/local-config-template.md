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

## Optional Helper Commands

```sh
python3 resume.py init-job --company "<Company>" --role "<Role>" --jd-file "<short-jd.md>"
python3 resume.py prepare-context --role-key "<company-role>"
python3 resume.py build --company "<Company>" --role "<Role>" --require-one-page
python3 resume.py reset-baseline
```

`resume.py` should call `scripts/build_resume.sh` for compilation. It should not generate resume content or replace the agent's judgment.

## Validation Requirements

- compile must succeed
- PDF must exist in the final output folder
- page count must match the configured target
- log must not contain LaTeX errors
- log should not contain overfull/underfull warnings
- fonts should be embedded
- text should extract cleanly
