# Deployment Guide

## Streamlit Cloud Deployment

1. Push this repository to GitHub.
2. Open Streamlit Cloud.
3. Click **New app**.
4. Select repository: `delivery-route-efficiency-dashboard`.
5. Select branch: `main`.
6. Set main file path: `streamlit_app.py`.
7. Click **Deploy**.

## Required Runtime Notes
- No PostgreSQL required.
- No external APIs required.
- No API keys or secrets required.
- No paid services required.

## Troubleshooting

### App shows no data
Run locally before deploy:
```bash
python scripts/generate_data.py
python scripts/build_sqlite_db.py
python scripts/validate_data.py
```

### Import errors on Cloud
- Ensure `requirements.txt` includes all dependencies.
- Confirm all modules are committed under `src/`.

### Build timeout
- Verify no network-only dependencies are introduced.
- Keep data generation and SQLite build scripts deterministic and local.

### Streamlit entrypoint error
- Confirm app path is exactly `streamlit_app.py`.
