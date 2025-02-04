from playwright.sync_api import sync_playwright
import os
from typing import Optional
from dotenv import load_dotenv
from nopecha.extension import build_chromium
import pathlib


def get_overleaf_session(email: str, password: str) -> Optional[str]:
    """Get Overleaf session2 cookie after login.
    
    Args:
        email: Overleaf account email
        password: Overleaf account password
        
    Returns:
        Session cookie value or None if login fails
    """
    # Only build nopecha extension if key is available
    nopecha_key = os.environ.get('NOPECHA_KEY')
    if nopecha_key:
        extension_path = build_chromium({
            "key": nopecha_key,
        }, pathlib.Path("nopecha_extension"))

        print(f"Using extension path: {extension_path}")
        extension_path = pathlib.Path(extension_path)
        if not extension_path.exists():
            raise RuntimeError(f"Extension path does not exist: {extension_path}")
        
        browser_args = [
            f"--disable-extensions-except={extension_path.absolute()}",
            f"--load-extension={extension_path.absolute()}"
        ]
    else:
        print("No NOPECHA_KEY found. You'll need to solve the captcha manually if it appears.")
        browser_args = []

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(pathlib.Path.home() / ".playwright-chrome-data"),
            headless=False,
            args=browser_args
        )
        
        page = browser.new_page()
        page.goto('https://www.overleaf.com/login')
        
        if not '/login' in page.url:
            print("Already logged in!")
            cookies = browser.cookies()
            session_cookie = next(
                (cookie for cookie in cookies if cookie["name"] == "overleaf_session2"),
                None
            )
            browser.close()
            return session_cookie["value"] if session_cookie else None

        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        
        page.click('button[type="submit"]')
        
        try:
            page.wait_for_url('https://www.overleaf.com/project', timeout=30000)
        except:
            if '/login' in page.url:
                if not nopecha_key:
                    print("Please solve the captcha manually...")
                page.wait_for_load_state('networkidle', timeout=300000)  # 5 minutes timeout for manual solving
                page.wait_for_timeout(5000)

        cookies = browser.cookies()
        session_cookie = next(
            (cookie for cookie in cookies if cookie["name"] == "overleaf_session2"),
            None
        )
        browser.close()
        return session_cookie["value"] if session_cookie else None


if __name__ == "__main__":
    load_dotenv()
    
    email = os.environ.get("OVERLEAF_EMAIL")
    password = os.environ.get("OVERLEAF_PASSWORD")
    
    if not email or not password:
        raise ValueError("Please set OVERLEAF_EMAIL and OVERLEAF_PASSWORD environment variables")
        
    session = get_overleaf_session(email, password)
    if session:
        print(f"overleaf_session2={session}")
    else:
        print("Failed to get session cookie")