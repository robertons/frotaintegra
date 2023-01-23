
def LoadLayout(Browser):
    print("\t\u2714 Carregando Modulos\n")
    Browser.headers.update({ 'Origin': 'https://www.frotasaas.com.br', 'Referer': 'https://www.frotasaas.com.br/frotaweb/Telas/tl10320.asp'})
    Browser.get('https://www.frotasaas.com.br/frotaweb/default.asp')
    Browser.headers.update({ 'Origin': 'https://www.frotasaas.com.br', 'Referer': 'https://www.frotasaas.com.br/frotaweb/default.asp'})
    Browser.get('https://www.frotasaas.com.br/frotaweb/topo.asp')
    Browser.get('https://www.frotasaas.com.br/frotaweb/telas/menuusuario.asp')
    Browser.get('https://www.frotasaas.com.br/frotaweb/menu/menutrei.xml')
    Browser.get('https://www.frotasaas.com.br/frotaweb/home.asp')
