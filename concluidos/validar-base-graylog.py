from os import getenv
from playwright.sync_api import sync_playwright
import time
import json

def autenticar():
    graylog = navegador.new_page()
    graylog.goto('http://logs-dash.zitausch.com:9000/streams/5de90061913ecb0854c57900/search?rangetype=relative&fields=message%2Csource&width=1920&highlightMessage=&relative=172800&q=')
    usuario = getenv(key='USUARIO_GRAYLOG')
    senha = getenv(key='SENHA_GRAYLOG')
    graylog.fill('div.form-group:nth-child(2) > span:nth-child(1) > input:nth-child(1)', usuario)
    graylog.fill('div.form-group:nth-child(3) > span:nth-child(1) > input:nth-child(1)', senha)
    graylog.locator('xpath=/html/body/div/div/div/div/form/div[3]/button').click()
    time.sleep(2)
    return graylog

def abrir_arquivo(arquivo):
    with open(arquivo, 'r') as file:
        arquivo = file.read().split()
        return arquivo

def consultar(arquivo):
    try:
        arquivo = abrir_arquivo(arquivo)
    except:
        print("Caminho do arquivo passado de forma incorreta.")
        return
    graylog = autenticar()
    print('SEMPRE QUE APARECER "..." NA TELA, PRESSIONE ENTER PARA CAPTURAR A 1° MENSAGEM DO GRAYLOG OU ESCREVA A MENSAGEM QUE DESEJA PRINTAR\n')
    consulta1 = " AND operacao:base" #consulta padrão
    #consulta1 = " AND SourceMethodName:fetchBaseProdutosFornecedor" #consulta personalizavel (comentar a linha)
    for cnpj in arquivo:
        cnpj_consulta = cnpj + consulta1
        load = False
        while load == False:
            time.sleep(0.5)
            load = graylog.locator(
                'button.btn-success:nth-child(1)').is_visible() #caso onde usando o xpath o caminho é alterado, mas usando o css o caminho permanece o mesmo
            time.sleep(0.5)
        time.sleep(0.5)
        graylog.goto(f'http://logs-dash.zitausch.com:9000/streams/5de90061913ecb0854c57900/search?rangetype=relative&fields=source%2Ccrawler'
                     f'%2Cmessage&width=1920&highlightMessage=&relative=172800&q={cnpj_consulta}') #realizar a consulta por parametro na URL
        time.sleep(3)
        not_found = graylog.locator('.description > a:nth-child(1)').is_visible() #valida se é possivel ver o NOT FOUND (bool)

        if not_found == False:

            # mensagem = graylog.locator(
            #     'xpath=/html/body/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[6]/div[3]/div/div/table/tbody[1]').text_content() #
            # mensagem = mensagem.split()[4::] #
            # mensagem = ' '.join(mensagem) #
            # print(f'{mensagem} - {cnpj}') #pegar a mensagem com a consulta personalizada (comentar as linhas)
            # if not mensagem: #

            qtd_jsons = graylog.locator('xpath=/html/body/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[6]/div[3]/div/div/table/tbody').count()
            diminuir = qtd_jsons
            time.sleep(1.5)
            if qtd_jsons != 1 | qtd_jsons != 0:
                print(f'Foram encontrados {qtd_jsons} jsons de base para o Cnpj: {cnpj_consulta}')
            lista_usuarios = ''

            while diminuir <= qtd_jsons:
                if diminuir > 0:
                    json_base = graylog.locator(
                        f'xpath=/html/body/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[6]/div[3]/div/div/table/tbody['
                        f'{diminuir}]/tr[2]/td/div').text_content()
                    json_base = json.loads(json_base)
                    usuario = json_base['usuario']
                    lista_usuarios += usuario + '\n'
                    diminuir -= 1
                if diminuir == 0:
                    break

            lista_usuarios = lista_usuarios.split()
            for usuario in lista_usuarios:
                consulta2 = 'operacao:base_produtos AND '
                usuario_consulta: str = consulta2 + '"' + usuario + '"'
                graylog.goto(f'http://logs-dash.zitausch.com:9000/streams/5de90061913ecb0854c57900/search?rangetype=relative&fields=source%2Ccrawler'
                             f'%2Cmessage&width=1920&highlightMessage=&relative=172800&q={usuario_consulta}') #consultar no log com o usuario do json
                load = graylog.locator(
                    '.message-result-fields-range > a:nth-child(1)').is_visible()

                while load == False:
                    time.sleep(0.5)
                    load = graylog.locator(
                        'button.btn-success:nth-child(1)').is_visible()

                not_found_usuario = graylog.locator('xpath=/html/body/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[4]/h1').is_visible()  # valida se é possivel ver o NOT FOUND (bool)

                if not_found_usuario == True:
                    mensagem = graylog.locator(
                        'xpath=/html/body/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[6]/div[3]/div/div/table/tbody[1]').text_content()
                    mensagem = mensagem.split()[4::]
                    mensagem = ' '.join(mensagem)
                    time.sleep(1)
                    # print(f'{mensagem}')
                    # print(f'Mensagem no Graylog: {mensagem} - {cnpj} - com o usuario - {usuario}')
                    validacao_mensagem = input('...')
                    if not validacao_mensagem:
                        print(f'Mensagem no Graylog: {mensagem} - {cnpj} - com o usuario - {usuario}')
                    if validacao_mensagem:
                        print(f'Mensagem no Graylog: {validacao_mensagem} - {cnpj} - com o usuario - {usuario}')

                if not_found_usuario == False:
                    cnpj = cnpj.split()[0]
                    #print(f"Processo não iniciou")
                    print(f"Processo não iniciou - {cnpj}")

        if not_found == True:
            cnpj = cnpj.split()[0]
            # print("não localizado nos logs")
            print(f"Não localizado nos logs - {cnpj}")
            continue

    return

with sync_playwright() as p:
    ##### VARIAVEIS DO PLAYWRIGHT #####
    navegador = p.firefox.launch(
        headless=False)  # por padrão esse modo é headless = True (não mostra o navegador abrindo)
    ###################################
    arquivo = input("insira o nome do arquivo com os fornecedores para consultar: ")
    try:
        consultar(arquivo)
    except:
        print("Finalizando a automação...")