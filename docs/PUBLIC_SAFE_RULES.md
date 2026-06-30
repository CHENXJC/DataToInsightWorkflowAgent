# Public-safe Rules

## Core Rules

1. Use synthetic demo data by default.
2. Do not read `.env`, token, credential, secret, password, API key, or private config files.
3. Do not process real sensitive personal data.
4. Do not connect Gmail, Google Drive, Notion, real webpages, OCR, PDF ingestion, or external accounts in D2I-001.
5. Do not execute real external actions.
6. Do not auto git add / commit / push.
7. Keep generated outputs out of the public repo by default.
8. Keep `outputs/.gitkeep` only for public showcase.
9. Keep demo data explainable, synthetic, and safe for GitHub.
10. Do not claim real connector support before it exists.

## Forbidden Public Files

- `.env`
- `*.env`
- `token.json`
- `credentials.json`
- `client_secret*.json`
- `*.key`
- `*.pem`
- private screenshots
- real customer exports
- real client reports
- generated PDF / Word / CSV reports with private data
- large raw media files

## Demo Data Rules

Demo data may imitate realistic scenarios but must be fully synthetic. It can describe fake SME feedback, fake restaurant operation issues, fake job descriptions, and fake project notes, but cannot include real private material.

## Output Rules

Generated reports should go under `outputs/`. By default, `.gitignore` excludes generated files under `outputs/*` and keeps only `outputs/.gitkeep`.

## README Claims

README must clearly state current stage and avoid overstating capabilities. D2I-001 is planning and contract only, not a working full pipeline.
