
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import random
import pandas as pd
    
user_agent_list = [
'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
]
nombres = list()
url = list()
skus = list()
listas = []

def buscador():
    
    
    global listas, user_agent_list
    opts = Options()
    user_agent = random.choice(user_agent_list)
    opts.add_argument(user_agent)
    opts.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    desde = int(input("Ingrese el código desde que desea iterar\n"))
    ha = int(input("Ingrese el código hasta que desea iterar\n"))
    num = desde-1
    hasta = ha
    lineas = hasta-desde
    for i in range(hasta):
        
        num = num+1
        search = 'https://www.nike.cl/checkout/cart/add?sku={}&qty=1&seller=1&redirect=true&sc=1'.format(num)
        listas.append(search)
        
        driver= webdriver.Chrome('./chromedriver.exe', chrome_options=opts)
        if num == hasta:
            break
        else:
            if search in listas:
                driver.get(search)
                sleep(random.uniform(3.0, 5.0))
                print("--- CICLO  " + str(i+1)+"---")
                lin = i+1
                print("Entrando en oraculus")            
            
                nike = driver.find_elements(By.XPATH,'//*[@id="checkoutMainContainer"]/div[5]/div[3]/div[1]/div[2]/div/div[3]/div[2]/div/div[2]/div/table/tfoot/tr')
                car_vacio = driver.find_elements(By.XPATH, '//*[@id="cartLoadedDiv"]')
                
                for car in car_vacio:
                    link = str(search)
                    anuncio = car.find_element(By.XPATH, '//*[@id="cartLoadedDiv"]/div[1]/h2').text
                    if (anuncio == 'SU CARRITO ESTÁ VACIO'):
                        
                        print(anuncio)
                        nombres.append(anuncio)
                        url.append(link)
                        skus.append(num)
                    else:
                        for zap in nike:
                            product_tittle = zap.find_element(By.XPATH,'//*[@id="product-name{}"]'.format(num)).text
                            titulo = zap.find_element(By.XPATH, '//*[@id="checkoutMainContainer"]/div[5]/div[3]/div[1]/div[2]/div/div[3]/div[2]/div/div[2]/div/table/tfoot/tr/td[1]').text
                            precio = zap.find_element(By.XPATH, '//*[@id="checkoutMainContainer"]/div[5]/div[3]/div[1]/div[2]/div/div[3]/div[2]/div/div[2]/div/table/tfoot/tr/td[3]').text
                            link = str(search)
                            if (precio == 'Por calcular'):
                                print('Aun no suben stock')
                                print(product_tittle+ ' \n '+ titulo + ' precio: ' +precio)
                                nombres.append(product_tittle)
                                url.append(link)
                                skus.append(num)
                                print('URL: '+link)
                            else:
                                nombres.append(product_tittle)
                                url.append(link)
                                skus.append(num)
                                print(product_tittle+ ' \n '+ titulo + ' precio: ' +precio)
                                print('URL: '+link)
                                print('****\n'+'identificador'+'\n*******')
                            time.sleep(random.uniform(2.0, 4.0))
    df = pd.DataFrame({'Nombre' : nombres, 'Links': url, 'Sku' : skus}, index= None)
    print(df)
    
while True:
    buscador()