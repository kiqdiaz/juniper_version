import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = 'https://supportportal.juniper.net/s/article/Junos-Software-Versions-Suggested-Releases-to-Consider-and-Evaluate?language=en_US'

def get_juniper_info(modelos):
    # session = HTMLSession()
    # response = session.get(url)
    # response.html.render()
    options = Options()
    options.headless = True
    response = webdriver.Chrome(options=options)
    response.get(url)
    time.sleep(10)
    soup = BeautifulSoup(response.page_source, 'html.parser')
    tables = soup.find_all('table', {'summary': 'EX Series Ethernet Switches'})
    headers = []
    informacion = []
    for i,table in enumerate(tables):
        # print('*'*20)
        # print(str(i), table.get_text(strip=True))
        trs = table.find_all('tr')
        encabezados = [] 
        for j, tr in enumerate(trs):
            # print(str(i), str(j), tr.get_text(strip=True))
            diccionario = {}
            valores = []
            ths = tr.find_all('th')
            if not encabezados: encabezados = [x.get_text(strip=True) for x in ths]
            tds = tr.find_all('td')
            if not valores:
                valores = [x.get_text(strip=True) for x in tds]
                diccionario2 = dict(zip(encabezados, valores))
                # print(str(i), str(j), diccionario2)
                if diccionario2 != {}: 
                    # print("aca?")
                    # print(modelos)
                    for mod in modelos:
                        # print(mod)
                        # print(f'{mod.lower()} in {diccionario2["Platform"].lower()} ?',file=sys.stdout)
                        if mod.lower() in diccionario2['Platform'].lower():
                            diccionario.update({'model':diccionario2['Platform'],
                                            'brand': 'juniper',
                                            'latest_version': diccionario2['Junos Software by Platform'],
                                            'last_updated_version': diccionario2['LastUpdated'],
                                            'release_notes': diccionario2['Notes'],
                                            'url': url,
                                            })
            del valores
            if diccionario != {}: informacion.append(diccionario)
            del diccionario

    return informacion



if __name__ == "__main__":
    modelos = sys.argv[1:]
    if not modelos: modelos = ['MX10003','PTX10004','QFX5120-32C','EX2200','SRX300']
    informacion = get_juniper_info(modelos)
    print(informacion)
    # curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8002/get_updates?brand=juniper
    

            