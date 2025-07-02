import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

urls = ['https://support.huawei.com/enterprise/en/routers/netengine%208000%20m8-pid-250517142/software?offeringId=252772223',
        # 'https://support.huawei.com/enterprise/en/routers/netengine-8000-pid-252772223/software',
        # 'https://support.huawei.com/enterprise/en/switches/s7700-s8700-s9700-s12700-s16700-pid-259602655/software',
        'https://support.huawei.com/enterprise/en/switches/cloudengine%20s12700e-8-pid-250450830/software?offeringId=259602655',
        'https://support.huawei.com/enterprise/en/switches/cloudengine-s12700e-4-pid-250450838/software?offeringId=259602655',
        'https://support.huawei.com/enterprise/en/switches/cloudengine%20s6730-h-v2-pid-253349373/software?offeringId=259602657',
        'https://support.huawei.com/enterprise/en/switches/cloudengine%20s6730-h48x6c-pid-250538951/software?offeringId=259602657',
        'https://support.huawei.com/enterprise/en/switches/cloudengine%20s5731-h24t4xc-pid-250387184/software?offeringId=259602657',
        'https://support.huawei.com/enterprise/en/switches/s5730-36c-hi-24s-pid-23474113/software?offeringId=259602657',
        # 'https://support.huawei.com/enterprise/en/switches/s3700-s5700-s6700-pid-259602657/software'
        ]

def get_huawei_info(modelos):
    # session = HTMLSession()
    # session.headers.update({
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # })
    # response = session.get(url)
    # response.html.render(timeout=120)
    informacion = []
    diccionario = {}
    for url in urls:
        # print('*'*20)
        options = Options()
        options.headless = True
        response = webdriver.Chrome(options=options)
        response.get(url)
        time.sleep(10)  # Wait for the page to load completely
        soup = BeautifulSoup(response.page_source, 'html.parser')
        values = soup.find_all('div',{'class': 'el-table__inner-wrapper'})
        modelowebraw = soup.find_all('div', {'id': 'header-wrap'})
        for i, valores in enumerate(modelowebraw):
            valor = valores.find_all('div',{'class':'title'})
            for j, val in enumerate(valor):
                # print(str(i),str(j),val.get_text(strip=True))
                modeloweb = val.get_text(strip=True)
        diccionario = {}
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
                    diccionario2 = dict(zip(encabezados, valores))
                    if diccionario2 != {}: 
                        if 'Version and Patch Number' in diccionario2.keys():
                            diccionario.update({'model':modeloweb,
                                            'brand': 'huawei',
                                            'url': url,
                                            'latest_version': diccionario2['Version and Patch Number'],
                                            'last_updated_version': diccionario2['Publication Date'],
                                            })
                        else:
                            diccionario.update({'model':modeloweb,
                                            'brand': 'huawei',
                                            'latest_patch': diccionario2['Patch Number'],
                                            'last_updated_patch': diccionario2['Publication Date'],
                                            })
                del valores
        informacion.append(diccionario)
        del diccionario
                
    return informacion

if __name__ == "__main__":
    modelos = sys.argv[1:]
    if not modelos: modelos = ['S6730-H-V2','S6730-H','S5731-H']
    informacion = get_huawei_info(modelos)
    for i in informacion:
        print('*'*20)
        print(i)