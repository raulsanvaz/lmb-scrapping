from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar opciones de Chrome
options = Options()
options.add_argument("--headless")  # Ejecutar en modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Crear el driver usando webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Acceder a un sitio web
driver.get("https://www.lmb.com.mx/estadisticas")

# Imprimir el título de la página
print(driver.title)

# Cerrar el navegador
driver.quit()
