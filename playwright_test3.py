from playwright.sync_api import sync_playwright  # bibliotek (browser-automatisering)
from q_haderslev_vbo.playwright.playwright_debughelper import PlaywrightDebugHelper  # klasse (helper)

dbg = PlaywrightDebugHelper(debug=True)  # objekt (debug slået til)

with sync_playwright() as p:  # context manager (lukker pænt)
    browser = p.chromium.launch(headless=True)  # browser (Chromium)
    context = browser.new_context(viewport={"width": 1280, "height": 800})  # context (browser-session)
    page = context.new_page()  # page (browser-fane)

    page.goto("https://www.haderslev.dk", wait_until="networkidle")  # goto (åbn side)
    dbg.screenshot(page, "haderslev_forside")  # screenshot (gem billede)

    browser.close()  # close (luk browser)