from playwright.sync_api import sync_playwright  # bibliotek (færdig funktionalitet)

def duckduckgo_search():  # funktion (genbrugelig kodeblok)
    with sync_playwright() as p:  # context manager (sikker opsætning)
        browser = p.chromium.launch(headless=True)  # browser (uden GUI)
        page = browser.new_page()  # page (browser-fane)

        page.goto("https://duckduckgo.com")  # goto (åbn webside)

        page.wait_for_selector("input[name='q']")  
        # selector (vælger HTML-element)

        page.screenshot(path="duckduckgo_startside.png")  

        page.fill("input[name='q']", "Playwright Python")  
        # fill (skriv tekst)

        page.keyboard.press("Enter")  
        # press (tryk tast)

        page.wait_for_load_state("networkidle")  
        # networkidle (side færdig)

        page.screenshot(path="duckduckgo_result.png")  
        # screenshot (gem billede)

        print("Titel:", page.title())  
        # print (vis status)

        browser.close()  # close (luk browser)

if __name__ == "__main__":  # main guard (kør direkte)
    duckduckgo_search()
