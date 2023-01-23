
from bs4 import BeautifulSoup

def LoadSession(Browser, imprimir=False):
    if imprimir:
        print("\t\u2714 Configurando Sessão!\n")
    Browser.headers.update({'Origin': 'https://www.frotasaas.com.br', 'Referer':'https://www.frotasaas.com.br/frotaweb/topo.asp'})
    DadosSessao = Browser.get('https://www.frotasaas.com.br/frotaweb/telas/carregasessions.asp')
    soup = BeautifulSoup(DadosSessao.content, "html.parser")
    payload_session = {input.attrs.get("name"):input.attrs.get("value", "") for input in soup.find_all("input")}
    Browser.headers.update({'Origin':'https://www.frotasaas.com.br', 'Referer':'https://www.frotasaas.com.br/frotaweb/telas/carregasessions.asp'})
    Browser.post('https://www.frotasaas.com.br/frotaweb/Net/preenchesessions.aspx?url=', data=payload_session)
    return payload_session

def CheckSession(Browser):
    req = Browser.get('https://www.frotasaas.com.br/frotaweb/verificaSessao.asp')
    return req
