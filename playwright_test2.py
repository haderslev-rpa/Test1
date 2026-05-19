from playwright.sync_api import sync_playwright  # bibliotek (browser-automatisering)
from datetime import datetime  # modul (dato og tid)
from pathlib import Path  # klasse (arbejde med mapper)

# ---------- KONFIGURATION ----------
BASE_DEBUG_DIR = Path("Debug")  # mappe (samler kørsler)

URLS = [
    ("haderslev", "https://www.haderslev.dk"),
    ("min-organisation", "https://intranet.haderslev.dk/min-organisation"),
    ("hjaelp-til-alle", "https://intranet.haderslev.dk/hjaelp-til-alle"),
]
# ----------------------------------


def get_next_debug_folder():  # funktion (genbrugelig kodeblok)
    BASE_DEBUG_DIR.mkdir(exist_ok=True)  # metode (opret mappe)

    existing = [
        p for p in BASE_DEBUG_DIR.iterdir()
        if p.is_dir() and p.name.startswith("Debug_")
    ]  # liste (samling af mapper)

    numbers = []
    for folder in existing:
        try:
            numbers.append(int(folder.name.replace("Debug_", "")))
        except ValueError:
            pass

    next_number = max(numbers, default=0) + 1
    debug_folder = BASE_DEBUG_DIR / f"Debug_{next_number}"
    debug_folder.mkdir()

    return debug_folder


def timestamp():  # funktion (tid som tekst)
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def accept_cookies_if_present(page):  # funktion (cookie-håndtering)
    try:
        banner = page.locator("#coi-banner-wrapper")  # locator (finder banner)

        # Vent kort på at banneret overhovedet findes
        banner.wait_for(state="visible", timeout=8000)  # wait_for (vent synlig)

        # BEDSTE METODE: role/aria + exact + scoped til banner
        ok_button = banner.get_by_role("button", name="OK", exact=True)  # role-finder (knap)
        ok_button.wait_for(state="visible", timeout=8000)  # wait_for (vent synlig)
        ok_button.click()  # click (klik knap)

        print("✅ Cookies accepteret")
        page.wait_for_timeout(800)  # wait (kort pause)

    except Exception as e:
        # Fallback (backup): klik via CSS hvis role/aria driller
        try:
            banner = page.locator("#coi-banner-wrapper")  # locator (finder banner)
            banner.locator("button.coi-banner__accept[aria-label='OK']").click(timeout=3000)  # CSS (backup)
            print("✅ Cookies accepteret (CSS backup)")
            page.wait_for_timeout(800)  # wait (kort pause)
        except Exception:
            print("ℹ️ Cookie-popup ikke håndteret:", e)


def run():  # funktion (styrer flow)
    debug_folder = get_next_debug_folder()  # objekt (kørselsmappe)
    print(f"Kører i mappe: {debug_folder}")

    with sync_playwright() as p:  # context manager (lukker pænt)
        browser = p.chromium.launch(headless=True)  # browser (chromium)

        context = browser.new_context(
            viewport={"width": 1280, "height": 800}  # viewport (skærmstørrelse)
        )  # context (browser-session)

        page = context.new_page()  # page (browser-fane)

        for index, (name, url) in enumerate(URLS, start=1):
            print(f"Går til: {url}")

            page.goto(url, wait_until="networkidle")  # goto (åbn side)

            accept_cookies_if_present(page)  # funktion (accepter cookies)

            file_name = f"{index:02d}_{timestamp()}_{name}.png"
            screenshot_path = debug_folder / file_name

            page.screenshot(path=str(screenshot_path), full_page=True)  # screenshot (gem billede)
            print(f"Screenshot gemt: {screenshot_path}")

        browser.close()  # close (luk browser)


if __name__ == "__main__":  # main guard (kør direkte)
    run()
