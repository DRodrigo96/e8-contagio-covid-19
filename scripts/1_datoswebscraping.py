
# PARTE 1: SELENIUM PARA DESCARGAR DATOS

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

path = r'C:\Users\RODRIGO\Desktop\MinsaData'
link = 'https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa'
xpath = '//*[@id="data-and-resources"]/div/div/ul/li/div/span/a'

options = webdriver.ChromeOptions()
preferences = {'download.default_directory': path, 'safebrowsing.enabled': 'false'}

options.add_experimental_option ('prefs', preferences)

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

driver.get(link)
driver.find_element(By.XPATH, xpath).click()

x = int()
while x < 120: 
    time.sleep(10)
    x += 10
    print('Tiempo restante:', 120-x, 'segundos')

driver.close()