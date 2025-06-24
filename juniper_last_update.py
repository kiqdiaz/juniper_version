import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession

url = 'https://supportportal.juniper.net/s/article/Junos-Software-Versions-Suggested-Releases-to-Consider-and-Evaluate?language=en_US'

def get_juniper_info(modelos):
    session = HTMLSession()
    response = session.get(url)
    response.html.render()
    soup = BeautifulSoup(response.html.html, 'html.parser')
    tables = soup.find_all('table', {'summary': 'EX Series Ethernet Switches'})
    headers = []
    informacion = []
    for i,table in enumerate(tables):
        aux = table.find_all('tr')
        for j, tabl in enumerate(aux):
            aux2 = tabl.find_all('td')
            if not headers:
                aux3 = tabl.find_all('th')
                for h in aux3:
                    headers.append(h.get_text(strip=True))
            texto1 = tabl.get_text(strip=True)
            for modelo in [x.lower() for x in modelos]:
                if modelo in texto1.lower():
                    valores = []
                    for k, tab in enumerate(aux2):
                        texto2 = tab.get_text(strip=True)
                        valores.append(texto2)
                    informacion.append(dict(zip(headers, valores)))
                    # print(dict(zip(headers, valores)))
    return informacion



if __name__ == "__main__":
    modelos = sys.argv[1:]
    if not modelos: modelos = ['MX10003','PTX10004','QFX5120-32C']
    informacion = get_juniper_info(modelos)
    print(informacion)
    

            