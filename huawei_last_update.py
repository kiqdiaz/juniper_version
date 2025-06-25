import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

urls = ['https://support.huawei.com/enterprise/en/routers/netengine-8000-pid-252772223/software',
        'https://support.huawei.com/enterprise/en/switches/s7700-s8700-s9700-s12700-s16700-pid-259602655/software',
        'https://support.huawei.com/enterprise/en/switches/s3700-s5700-s6700-pid-259602657/software']

def get_huawei_info(modelos):
    # session = HTMLSession()
    # session.headers.update({
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # })
    # response = session.get(url)
    # response.html.render(timeout=120)
    informacion = []

    for url in urls:
        options = Options()
        options.headless = True
        response = webdriver.Chrome(options=options)
        response.get(url)
        time.sleep(10)  # Wait for the page to load completely
        soup = BeautifulSoup(response.page_source, 'html.parser')
        values = soup.find_all('div',{'class': 'el-table__inner-wrapper'})
        for i,valor in enumerate(values):
            trs = valor.find_all('tr')
            encabezados = []
            for j,tr in enumerate(trs):
                valores = []
                ths = tr.find_all('th')
                if not encabezados: encabezados = [x.get_text(strip=True) for x in ths]
                tds = tr.find_all('td')
                if not valores: 
                    valores = [x.get_text(strip=True) for x in tds]
                    diccionario = dict(zip(encabezados, valores))
                    if diccionario != {}: informacion.append(dict(zip(encabezados, valores)))
                    del valores
    return informacion

if __name__ == "__main__":
    modelos = sys.argv[1:]
    if not modelos: modelos = ['S6730-H-V2','S6730-H','S5731-H']
    informacion = get_huawei_info(modelos)
    for i in informacion:
        print('*'*20)
        print(i)