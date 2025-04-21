import asyncio
from playwright.async_api import async_playwright

class LMBStatistics:
    def __init__(self):
        self.browser = None
        self.page = None

    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.goto("https://www.lmb.com.mx/estadisticas", timeout=60000)

    async def get_players(self):
        await self.init_browser()
        # Imprimir el título de la página
        title = await self.page.title()
        print(f"Título de la página: {title}")
        # Hacer clic en "Jugadores"
        await self.page.locator("div:has-text('Jugadores')").first.click(force=True)
        await asyncio.sleep(2)
        # Hacer clic en "Bateo"
        await self.page.locator("div:has-text('Bateo')").first.click(force=True)
        await asyncio.sleep(2)
        # Seleccionar año 2010
        await self.page.locator("select").nth(0).select_option("2010")
        await asyncio.sleep(2)
        #flag = True
        players = []
        for i in range(0,10):
            players_aux = await self.get_table_data()
            players.append(players_aux[1])
            await self.page.locator("div:has-text('Próx')").first.click(force=True)
        print(players)

        # Cerrar navegador
        await self.browser.close()

    
    async def get_table_data(self):
        # Esperar la tabla
        await self.page.wait_for_selector("table.StatsLayout_entityTable__eKIac", timeout=10000)
        tabla = self.page.locator("table.StatsLayout_entityTable__eKIac")

        # Extraer encabezados desde la fila con clase `table-row-header`
        header_row = tabla.locator("tr.table-row-header")
        header_cells = await header_row.locator("th, td").all()  # A veces usan <td> como encabezado también
        headers = [await cell.inner_text() for cell in header_cells]

        # Extraer datos
        rows = await tabla.locator("tbody tr:not(.table-row-header)").all()
        data = []

        for row in rows:
            cells = await row.locator("td").all()
            values = [await cell.inner_text() for cell in cells]
            data.append(values)

        return headers, data

# Ejecutar
async def main():
    lmb = LMBStatistics()
    await lmb.get_players()

asyncio.run(main())
