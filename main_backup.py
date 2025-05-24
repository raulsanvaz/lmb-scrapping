import re
import os
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def getPlayers(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    years = ["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"]
    page = context.new_page()
    page.goto("https://lmb.com.mx/estadisticas")
    page.get_by_role("button", name="Aceptar todas las cookies").click()
    page.get_by_text("Jugadores", exact=True).nth(3).click()
    page.get_by_text("Bateo").nth(2).click()
    for year in years:
        print(f'Scrappeando {year}...')
        os.makedirs(os.path.join(os.getcwd(), 'downloads', 'images', year), exist_ok=True)
        page.locator(".CustomSelect_customSelect__7RjU5").first.select_option(year)
        flag = True
        pageCount = 0
        while flag:
            try:
                time.sleep(5)
                page.screenshot(path=os.path.join(os.getcwd(), 'downloads', 'images', year, f'year-{pageCount}.png'), full_page=True)
                page.get_by_text("Próx").nth(2).click()
                pageCount += 1
            except Exception as ex:
                print(ex)
                flag = False
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    getPlayers(playwright)