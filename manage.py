import selenium
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # Necesario para buscar elementos dentro del HTML
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EXP_COND

# 0. URL a la que vamos a acceder
url="https://google.com"

# 1. Llamamos al path del webdriver y creamos el servicio de chrome
path = "/Applications/driver_sel/chromedriver-mac-arm64/chromedriver"
chrome_service = Service(executable_path=path)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("--headless")

# 2. Creamos la instancia de nuestro driver y modificamos el tamaño de la ventana
driver = webdriver.Chrome(service=chrome_service, options=options)
window_width = 550
window_height = 950
driver.set_window_size(window_width, window_height)

# 3. Podemos empezar a scrappear!
driver.get(url)
driver.implicitly_wait(0.4)

# Aceptamos política de cookies de google:
try:
    accept_cookies = driver.find_element(By.XPATH, value='/html/body/div[2]/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[2]')
    accept_cookies.click()
    print("Aceptamos la política de cookies")
except Exception as e:
    print("Ha ocurrido un error ->", type(e).__name__, e)


# Método para poder esperar a que los elementos del DOM carguen. En este caso, esperamos 5 segundos
WebDriverWait(driver, 5).until(
    EXP_COND.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)

### Buscamos en searchbar de google
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.clear() # Limpiamos el posible string de texto que exista en el input.
input_element.send_keys("el pais periodico" + Keys.ENTER) # Introducimos el texto que deseamos buscar

# Hacemos click en el link por su texto
link = driver.find_element(By.PARTIAL_LINK_TEXT, "El País")
link.click() # redirects!


# Aceptamos las cookies del sitio para poder continuar
try:
    cookies_elpais = driver.find_element(By.XPATH, value='/html/body/div[5]/div/div/div/div[2]/div[1]/a')
    cookies_elpais.click()
    print("Aceptamos las cookies de El País")
except Exception as e:
    print("Ha ocurrido un error ->", type(e).__name__, e)


#### Vamos a capturar los titulares del día #### find_elements() devuelve un array ####
"""Para poder capturar los titulares del día, primero, tenemos que conocer el número de artículos que existen y de cada uno de ellos, acceder al titular.
Por tanto, podemos plantearlo como un loop for"""

WebDriverWait(driver, 2).until(
    EXP_COND.presence_of_element_located((By.CLASS_NAME, "c_t"))
)
# Recuperamos el número de artículos de la página de El País : /html/body/div[2]/main/div[1]/section/div[2]/article[1]/header/h2/a
num_articulos = len(driver.find_elements(By.TAG_NAME, value="article"))
print("Este es el número de artículos del periódico: ", num_articulos)

# Bucle for para recopilar los titulares ----> ES ERRÓNEO YA QUE EL XPATH CAMBIA
# for i in range(1, num_articulos + 1):
#     try:
#         xpath = "/html/body/div[2]/main/div[1]/section/div[1]/article[{}]/header/h2/a".format(i)
#         # Esperamos al elemento...
#         time.sleep(3)
#         resultado = driver.find_element(By.XPATH, value=xpath)
#         titular = resultado.text
#         titulares_EL_PAIS.append(titular)
#     except Exception as e:
#         print(e, type(e).__name__)

titulares_EL_PAIS = driver.find_elements(By.TAG_NAME, value="article")


print("\n------ Los titulares del periódico EL PAÍS ------")
for index, titular in enumerate(titulares_EL_PAIS):
    print("\n\t- {}: {}.".format(index, titular))


time.sleep(1000)

# driver.close() # .close() para cerrar la tab /// .quit() para cerrar el browser