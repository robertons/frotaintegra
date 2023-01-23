
import json

def LoginFrota(Browser, user_data):

    print("\t\u2714 Identificando Empresa\n")

    # CARREGA LOGIN
    Browser.get('https://www.frotasaas.com.br/frotaweb/Telas/TL10320.asp')

    # PAYLOAD LOGIN DE EMPRESA
    payload_empresa = {
            'hidpwd': '',
            'txtcd_empresa': user_data['codigo'],
            'txtcd_usuario': 0,
            'txtcd_recurso': 0,
            'txtcd_filial': 0,
            'pwdsenha': '',
            'hidpwd': ''
    }

    print("\t\u2714 Realizando Login\n")
    Browser.post('https://www.frotasaas.com.br/frotaweb/Telas/tl10320.asp?acao=cd_empresa', data=payload_empresa)

    payload_empresa['txtcd_usuario'] = user_data['usuario']
    payload_empresa['txtcd_filial'] = user_data['filial']
    payload_empresa['pwdsenha'] = user_data['pass']
    payload_empresa['hidpwd'] = user_data['pass']

    Browser.headers.update({'Origin': 'https://www.frotasaas.com.br', 'Referer': 'https://www.frotasaas.com.br/frotaweb/Telas/tl10320.asp' })

    Browser.post('https://www.frotasaas.com.br/frotaweb/Telas/tl10320.asp', data=payload_empresa)
