# Overleaf Cookie Obtainer

A Python script to programmatically obtain Overleaf session cookies, with optional automated CAPTCHA solving support via NopeCHA.
It will output a string of the form `overleaf_session2=<cookie>` for usage in [Overleaf Workshop VSCode Extension](https://github.com/iamhyc/Overleaf-Workshop).

## Setup
I suggest using [uv](https://github.com/astral-sh/uv)
1. Install dependencies:
```bash
uv sync
uv run playwright install
```

2.Create `.env` file:
```
OVERLEAF_EMAIL=your@email.com
OVERLEAF_PASSWORD=your_password
NOPECHA_KEY=your_nopecha_key  # Optional, for automated CAPTCHA solving
```

## Usage
```bash
uv run login.py
```

The script will:
- Launch a browser window
- Log into Overleaf
- Return the session cookie
- Handle CAPTCHAs automatically (if NOPECHA_KEY is provided) or wait for manual solving

## Notes

- Without a NOPECHA_KEY, you'll need to solve CAPTCHAs manually
- The script runs in headed mode (visible browser) due to extension requirements
