# Security And Privacy

Checkpoint: `D2I-006-SCREENSHOT-CAPTURE-AND-README-SCREENSHOT-UPDATE-COMPLETE`

## Default Mode

DataToInsightWorkflowAgent is local-first, demo-mode, and public-safe by default.

## Data Boundary

- Uses synthetic demo data only
- Does not process real customer files
- Does not process private personal notes
- Does not require account data
- Does not upload files
- Does not call external APIs

## Secret Boundary

The project does not require or read:

- `.env`
- API keys
- tokens
- credentials
- passwords
- private connector files

If any of these files are present locally, they must not be opened, printed, copied into docs, or committed.

## Connector Boundary

No real Gmail, Google Drive, Notion, web crawler, OCR/PDF, or LLM API connector is enabled in the current showcase version.

## Output Boundary

Generated files in `outputs/` are ignored by default through `.gitignore`. The public showcase may describe the demo report, but should not commit private outputs or large generated artifacts.

## Manual Review Before Release

Before any GitHub public release:

- Run `python tools/public_release_check.py`
- Run `python -m pytest -q`
- Run `python -m compileall .`
- Run the CLI demo
- Run a Streamlit smoke check
- Manually inspect README, docs, manifest, and screenshots
- Confirm no private path, token, credential, or real data is included
