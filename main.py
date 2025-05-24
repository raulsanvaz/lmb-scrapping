import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright


def scrapeTable(page):
    # Obtener el HTML completo de la página
    html = page.content()

    # Usar BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer encabezados de la tabla
    headers = []
    header_cells = soup.select("table thead tr td span.StatsHeaderColumn_columnData__MM9GT")
    for header in header_cells:
        headers.append(header.get_text().strip())

    # Extraer filas de datos de la tabla
    rows = soup.select("table tbody tr")
    data = []

    for row in rows:
        cells = row.find_all("td")
        player_name = cells[0].get_text().strip().replace("\n", " ")
        team_img = cells[1].find("img")["alt"] if cells[1].find("img") else ""
        stats = [cells[j].get_text().strip() for j in range(2, len(cells))]
        full_row = [player_name, team_img] + stats
        data.append(full_row)

    # Asegurarse de que los encabezados coincidan con el número de columnas
    headers = headers[:len(data[0])]  # En caso de que sobren columnas

    # Crear un DataFrame de pandas
    df = pd.DataFrame(data, columns=headers)
    return df


def getPlayers(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    years = ["2005", "2006", "2007", "2008", "2009", "2010", 
             "2011", "2012", "2013", "2014", "2015", "2016", 
             "2017", "2018", "2019", "2020", "2021", "2022", 
             "2023", "2024", "2025"]
    years = ["2005", "2006", "2007"]  # Filtrar algunos años para prueba
    page = context.new_page()
    page.goto("https://lmb.com.mx/estadisticas")

    # Aceptar cookies
    page.get_by_role("button", name="Aceptar todas las cookies").click()
    page.get_by_text("Jugadores", exact=True).nth(3).click()
    page.get_by_text("Bateo").nth(2).click()

    for year in years:
        print(f'Scrapeando {year}...')
        output_dir = os.path.join(os.getcwd(), 'downloads', 'data', year)
        os.makedirs(output_dir, exist_ok=True)
        page.locator(".CustomSelect_customSelect__7RjU5").first.select_option(year)
        page_count = 0
        flag = True

        all_data = []

        while flag:
            try:
                time.sleep(5)  # Asegura que la página cargue
                df = scrapeTable(page)  # Usar BeautifulSoup en lugar de Playwright directamente
                all_data.append(df)

                # Guardar screenshot
                screenshot_path = os.path.join(output_dir, f'year-{page_count}.png')
                page.screenshot(path=screenshot_path, full_page=True)

                # Pasar a la siguiente página
                page.get_by_text("Próx").nth(2).click()
                page_count += 1
            except Exception as ex:
                print(f"Fin de páginas para {year}. Total páginas: {page_count}")
                flag = False

        # Concatenar todos los datos del año y guardar CSV
        if all_data:
            df_year = pd.concat(all_data, ignore_index=True)
            df_year.to_csv(os.path.join(output_dir, f'estadisticas_{year}.csv'), index=False)
            print(f'Datos guardados para {year}: {len(df_year)} registros')

    context.close()
    browser.close()


with sync_playwright() as playwright:
    getPlayers(playwright)
