import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://lmb.com.mx/estadisticas")
    page.get_by_role("button", name="Aceptar todas las cookies").click()
    page.get_by_text("Jugadores", exact=True).nth(3).click()
    page.get_by_text("Bateo").nth(2).click()
    page.locator(".CustomSelect_customSelect__7RjU5").first.select_option("2005")
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura1.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura2.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura3.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura4.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura5.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura6.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura7.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura8.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura9.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura10.png", full_page=True)
    page.get_by_text("Próx").nth(2).click()
    page.screenshot(path="captura11.png", full_page=True)
    page.locator(".CustomSelect_customSelect__7RjU5").first.select_option("2006")
    page.screenshot(path="captura12.png", full_page=True)
    page.locator(".CustomSelect_customSelect__7RjU5").first.select_option("2007")
    page.screenshot(path="captura13.png", full_page=True)
    page.get_by_text("First").nth(2).click()
    page.locator("span").filter(has_text=re.compile(r"^2$")).nth(2).click()
    page.locator("span").filter(has_text=re.compile(r"^3$")).nth(2).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)