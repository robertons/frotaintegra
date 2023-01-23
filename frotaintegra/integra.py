import sys
import os
import requests
import time
from bs4 import BeautifulSoup
import json
import unidecode
import json
import inquirer
import frotaintegra.utils


def CreateFolder(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def CreateDefaultIntegra():
    CreateFolder('./utils')
    integra_lista = [
        {
            "nome": "GoodCard",
            "codigo": "14795",
            "pasta": "./goodcard"
        },
        {
            "nome": "CTF",
            "codigo": "14750",
            "pasta": "./ctf"
        },
        {
            "nome": "Ticket",
            "codigo": "14740",
            "pasta": "./ticket"
        },
        {
            "nome": "ComVoc\u00ea",
            "codigo": "14781",
            "pasta": "./comvoce"
        }
    ]
    json_object = json.dumps(integra_lista, indent=4)
    with open("./utils/integradoras.json", "w") as outfile:
        outfile.write(json_object)

    for Integracao in integra_lista:
        try:
            dir_path = Integracao['pasta']
            arquivos = [os.path.join(dir_path, path) for path in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, path))]
        except Exception as e:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            arquivos = []

    return integra_lista

def Config():

    print("\n\n [ SETUP INTEGRAÇÃO FROTASAAS ] \n\n")

    print("\t\u2714 Configurando Usuário/Empresa\n")
    try:
        with open('./utils/user.json') as f:
            integra_user = json.load(f)
    except Exception as e:
        CreateFolder('./utils')
        integra_user = {
            "codigo" : "",
            "usuario" : "",
            "filial" : "",
            "pass" : ""
        }

    codigo = input("\tInforme o código da Empresa:")
    usuario = input("\tInforme o código do Usuário:")
    filial = input("\tInforme o número da Filial:")
    password = input("\tInforme senha de acesso:")

    integra_user['codigo'] = codigo
    integra_user['usuario'] = usuario
    integra_user['filial'] = filial
    integra_user['pass'] = password

    json_object = json.dumps(integra_user, indent=4)
    with open("./utils/user.json", "w") as outfile:
        outfile.write(json_object)

    return integra_user

    print("\n\t\u2714 Dados salvos com sucesso!\n")

    print("\n\n-----------------------------------------------------\n\n")

def ProcessaIntegracao():

    print("\n\n  [ PROCESSAMENTO INTEGRAÇÃO FROTASAAS ] \n\n")

    print("\t\u2714 Carregando Integradoras\n")
    try:
        with open('./utils/integradoras.json') as f:
            integra_lista = json.load(f)
    except Exception as e:
        integra_lista = CreateDefaultIntegra()

    try:
        with open("utils/user.json") as f:
            user_data = json.load(f)
    except Exception as e:
        user_data = Config()

    with requests.Session() as Browser:

        frotaintegra.utils.SetHeaders(Browser)

        frotaintegra.utils.LoginFrota(Browser, user_data)

        check = frotaintegra.utils.CheckSession(Browser)

        if int(check.text) == 1:

            print("\t\u2714 Conectado com Sucesso!\n")

            frotaintegra.utils.LoadLayout(Browser)

            frotaintegra.utils.LoadSession(Browser, True)

            frotaintegra.utils.RealizaIntegracao(Browser, integra_lista)
            print("\n\n-----------------------------------------------------\n\n")
        else:
            print("\t\u2716 Não foi possível conectar, dados incorretos. Processo finalizado!\n")
            print("\n\n-----------------------------------------------------\n\n")


def NovaIntegracao():

    print("\n\n [ CADASTRO INTEGRAÇÃO FROTASAAS ] \n\n")

    print("\t\u2714 Carregando Integradoras\n")
    try:
        with open('./utils/integradoras.json') as f:
            integra_lista = json.load(f)
    except Exception as e:
        CreateDefaultIntegra()

    new = True
    while new:
        name = input("\tInforme o nome da Integradora:")

        valid=False
        while not valid:
            try:
                codigo = input("\tInforme o código de tela (somente numeros):")
                codigo = int(codigo)
                valid = True
            except Exception as e:
                print("\t\u2716 Informe apenas números.")
                valid = False

        pasta = unidecode.unidecode(name.replace(" ","").replace("-","").replace("_","").lower())

        integra_lista.append({
            "nome": name,
            "codigo": codigo,
            "pasta": pasta
        })

        if not os.path.exists(pasta):
            os.makedirs(pasta)

        nova = input("\n\tDeseja incluir outra integradora (s/n) ?")
        new = nova == 's'

        print("\n\n-----------------------------------------------------\n\n")

    json_object = json.dumps(integra_lista, indent=4)

    with open("./utils/integradoras.json", "w") as outfile:
        outfile.write(json_object)

    print("\n\t\u2714 Dados salvos com sucesso!\n\n")

def integra(args):

    print("\n\n [ INTEGRAÇÃO FROTASAAS ] \n\n")

    try:
        with open('./utils/integradoras.json') as f:
            integra_lista = json.load(f)
    except Exception as e:
        integra_lista = CreateDefaultIntegra()

    try:
        while True:

            questions = [
                inquirer.List(
                    "action",
                    message="MENU PRINCIPAL",
                    choices=["Importar Dados", "Cadastrar Intgradora", "Configurar Empresa", "Sair"],
                    carousel=True),
            ]

            answers = inquirer.prompt(questions)

            if answers['action'] == 'Sair':
                break

            if answers['action'] == "Configurar Empresa":
                print("\n-----------------------------------------------------\n")
                Config()

            if answers['action'] == "Cadastrar Intgradora":
                print("\n-----------------------------------------------------\n")
                NovaIntegracao()

            if answers['action'] == "Importar Dados":
                print("\n-----------------------------------------------------\n")
                ProcessaIntegracao()


        print("\n-----------------------------------------------------\n")
        print("\n \u2714 Finalizado\n\n")
    except KeyboardInterrupt:
        print("\n-----------------------------------------------------\n")
        print('\n \u2714 Finalizado pelo teclado!\n')
