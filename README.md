# Tamil Letter Helper

A small Flask website that converts common Sinhala / Romanized Sinhala inputs into Tamil letters.

## Run on your computer

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `python -m venv .venv`
4. Activate the environment:
   - Windows: `.venv\\Scripts\\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Run `pip install -r requirements.txt`
6. Run `python app.py`
7. Open http://127.0.0.1:5000

## Publish it online (Render)

1. Create a GitHub account if you do not have one.
2. Create a new GitHub repository and upload `app.py`, `requirements.txt`, `render.yaml`, and the `templates` folder.
3. Sign in to Render and choose **New + → Web Service**.
4. Connect your repository. Render should use the settings in `render.yaml`; otherwise use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Click **Deploy**. Render will provide a public URL after a successful deployment.

## Important limitation

This is a starter transliteration tool, not a full language translator. Tamil spelling depends on pronunciation and conventions, so review important outputs. Add more words to `KNOWN` in `app.py` to improve common-word accuracy.
