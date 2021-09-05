
# PARTE 1: SELENIUM PARA DESCARGAR DATOS

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

os.chdir("../")

path = os.getcwd() + '\\data'
link = 'https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa'
xpath = '//*[@id="data-and-resources"]/div/div/ul/li/div/span/a'

options = webdriver.ChromeOptions()
preferences = {
    'download.default_directory': path, 
    'safebrowsing.enabled': True,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,

}

options.add_experimental_option('prefs', preferences)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get(link)
driver.find_element(By.XPATH, xpath).click()

# Esperando 1 minuto para descarga...
x = int()
while x < (t:=60): 
    time.sleep(10)
    x += 10
    print('Tiempo restante:', t-x, 'segundos')

driver.close()

print('DESCARGA COMPLETADA')