from .sessions import *
from requests_toolbelt import MultipartEncoder
import random,string
import os
import shutil

def TrataResposta(pagecontent):
    soup = BeautifulSoup(pagecontent, "html.parser")
    scriptTags = soup.find_all('script')
    for script in scriptTags:
        tagContent = script.get_text()
        start_index = tagContent.find('function inicializa()')
        if start_index > 0:
            start_index = tagContent.find('{') + 1
            end_index = tagContent.find('}')
            script_data = tagContent[start_index:end_index]
            if "alert" in script_data:
                return script_data.replace("alert('","").replace("');","").strip()
                break
            elif "confirm" in script_data:
                script_data = script_data.replace("if (confirm(\"","").strip()
                end_index = script_data.find('\n')
                return "Os dados do arquivo foram importados, porém existem alguns registros que originaram erros"
                break

def RealizaIntegracao(Browser, ListaIntegradoras):
    AquivosEncontrados = 0
    for Integracao in ListaIntegradoras:
        try:
            dir_path = Integracao['pasta']
            arquivos = [os.path.join(dir_path, path) for path in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, path))]
        except Exception as e:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            arquivos = []
        if len(arquivos) > 0:
            print(f"\n\n\t[ INICIANDO PROCESSAMENTO {Integracao['nome'].upper()} ]")
            print(f"\t\t\u2714 {len(arquivos)} arquivos encontrados para importação de {Integracao['nome']}")

            AquivosEncontrados = AquivosEncontrados + len(arquivos)

            print(f"\t\t\u2714 Verificando {Integracao['nome']} | Código de Tela: TL{Integracao['codigo']}")

            CheckSession(Browser)

            pagina_upload = Browser.get(f"https://www.frotasaas.com.br/frotaweb/telas/TL{Integracao['codigo']}.asp")
            soup = BeautifulSoup(pagina_upload.content, "html.parser")
            form = soup.find("form")
            payload_processa_arquivo = {input.attrs.get("name"):input.attrs.get("value", "") for input in form.find_all("input")}

            print("\t\t\u2714 Requisitando Envio de Arquivo...")

            Browser.headers.update({'Origin': 'https://www.frotasaas.com.br', 'Referer': f"https://www.frotasaas.com.br/frotaweb/telas/TL{Integracao['codigo']}.asp"})
            pagina_chamaenvio = Browser.get('https://www.frotasaas.com.br/frotaweb/telas/chamaenviaarqcarga.asp')

            for arquivo in arquivos:
                print(f"\t\t\u2714 Processando arquivo: {arquivo.split('/')[-1]}")

                print("\t\t\u2714 Obtendo autorização para envio de Arquivo...")

                Browser.headers.update({'Origin': 'https://www.frotasaas.com.br', 'Referer': "https://www.frotasaas.com.br/frotaweb/telas/chamaenviaarqcarga.asp"})
                pagina_chamaenvio = Browser.get('https://www.frotasaas.com.br/frotaweb/telas/enviaarqcarga.asp')

                payload_upload = {
                    'destino': "../telas/enviaarqcarga.asp",
                    'arquivo': "CargaAbastec",
                    'LinkCarga': (arquivo.split('/')[-1], open(arquivo, 'rb'), "text/plain"),
                }
                boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
                multpart = MultipartEncoder(fields=payload_upload, boundary=boundary)

                print("\t\t\u2714 Enviando Arquivo...")
                Browser.headers.update({'Origin': 'https://www.frotasaas.com.br', 'Referer': 'https://www.frotasaas.com.br/frotaweb/telas/enviaarqcarga.asp', 'Content-Type': f"multipart/form-data; boundary={boundary}"})
                post_upload = Browser.post('https://www.frotasaas.com.br/frotaweb/upload/fileCarga.asp', data=multpart)

                print("\t\t\u2714 Solicitando processamento do arquivo")

                payload_session = LoadSession(Browser)

                payload_processa_arquivo = {
                    'hidstatusreg' : 0,
                    'hidnm_arq': payload_session['URL_SERVER_CARGA'],
                    'radSaida': 1
                }
                Browser.headers.update({'Origin': 'https://www.frotasaas.com.br', 'Referer': f"https://www.frotasaas.com.br/frotaweb/telas/TL{Integracao['codigo']}.asp", 'Content-Type': "application/x-www-form-urlencoded"})
                pagina_processamento = Browser.post(f"https://www.frotasaas.com.br/frotaweb/telas/TL{Integracao['codigo']}.asp", data=payload_processa_arquivo)

                print(f"\t\t\u2714 Processameto do arquivo {arquivo.split('/')[-1]} finalizado")

                mensagem_processamento = TrataResposta(pagina_processamento.content)
                print(f"\t\t\u2714 Resposta Processamento: {mensagem_processamento}")

                print(f"\t\t\u2714 Movendo arquivo para processados")
                path_processados = os.path.join(dir_path, "processados")
                if not os.path.exists(path_processados):
                    os.makedirs(path_processados)
                shutil.move(arquivo, os.path.join(path_processados, arquivo.split('/')[-1]))

            print(f"\t\t\u2714 Processo de {Integracao['nome']} finalizado")

    if AquivosEncontrados > 0:
        print(f"\t\u2714 Processo Finalizado para {AquivosEncontrados} arquivos\n\n")
    else:
        print("\t\u2716 Não há arquivos para processamento. Processo finalizado!\n\n")
