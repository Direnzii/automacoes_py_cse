from os import getenv
from playwright.sync_api import sync_playwright
import time
import io

list_not_client = []

def abrir_arquivo(nome='cnpjs.txt'):
    with open(nome) as file:
        arquivo = file.read().replace(",", ' ').split()
    return arquivo


def autenticar(site):
    site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')
    print("Inserindo as credenciais ...")
    time.sleep(0.5)
    usuario_demo = getenv(key="USUARIO_DEMO")
    senha_demo = getenv(key="SENHA_DEMO")
    usuario = getenv(key='USUARIO_OFICIAL')
    senha = getenv(key='SENHA_OFICIAL')
    site.fill('xpath=//*[@id="frmLogin:username"]', usuario)
    site.fill('xpath=//*[@id="frmLogin:password"]', senha)
    site.locator('xpath=//*[@id="frmLogin:loginButton"]').click()
    time.sleep(0.2)


def cliente_nao_encontrado(site):
    return site.locator('xpath=//*[@id="inputHiddenMessage"]').is_visible()


def verificar_se_ja_processou(cliente):
    condicao = cliente in abrir_arquivo('nao_tem_fornecedor.txt')
    condicao2 = cliente in abrir_arquivo('not_client.txt')
    condicao3 = cliente in abrir_arquivo('condicoes_salvas.txt')
    condicao4 = cliente in abrir_arquivo('erro_no_cliente.txt')
    if condicao == True or condicao2 == True or condicao3 == True or condicao4 == True:
        return True
    else:
        return False


def verificar_chat(site):
    return site.locator('xpath=/html/body/jdiv/jdiv/jdiv[3]/jdiv[1]/jdiv/jdiv').is_visible()

def entrar_na_tela_cond(site):
    manualmente = 'N'  # input('Deseja inserir as informações e ir até a aba Fornecedores, manualmente ? (S) (N): ')
    # cliente = input('Insira o cnpj do cliente: ')
    for cliente in abrir_arquivo():
        cnpj_cliente_arquivo = cliente
        validacao_processou = verificar_se_ja_processou(cliente)
        if not validacao_processou:
            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]/a/img').click()
            if manualmente == 'S' or manualmente == 's':
                input('Processo travado, insira as informações até e entra na aba FORNECEDORES, depois clique em Enter...')
            else:
                #cliente = '26246183000547' #############
                time.sleep(1)
                site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table'
                          '/tbody/tr[1]/td/div/div[2]/table/tbody/tr[2]/td[2]/input', cliente)
                time.sleep(4)
                validacao_chat = verificar_chat(site)
                if validacao_chat:
                    site.locator('xpath=/html/body/jdiv/jdiv/jdiv[3]/jdiv[1]/jdiv/jdiv').click()
                    time.sleep(1)
                site.locator('xpath=//*[@id="pesquisarUsuarios:btnPesquisar"]').click()
                time.sleep(1.5)
                validacao_cliente_existe = cliente_nao_encontrado(site)
                if validacao_cliente_existe == True:
                    list_not_client.append(cliente)
                    print(f'{cnpj_cliente_arquivo}: Não é cliente ou é filial')
                    with io.open('not_client.txt', 'a', encoding='utf-8') as file:
                        file.write(f'{cnpj_cliente_arquivo}\n')
                    continue
                editar = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                                      '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr').count()

                try:
                    if editar != 1 and editar > 0:
                        site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                                     '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[1]/td[6]/a').click()
                    if editar == 1:
                        site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                                     '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr/td[6]/a').click()
                except:
                    site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                                 '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[1]/td[6]/a').click()

                site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
                             '/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[8]/table/tbody/tr/td[2]'
                             '/table/tbody/tr/td/table/tbody/tr/td[2]').click()  # aba fornecedor
                try:
                    select_element = site.locator(
                        'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                        '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                        '/tr/td/div[2]/div[2]/span[1]/select')
                    select_handle = select_element.element_handle()
                    opcao_desejada = select_handle.query_selector('option[value="6453"]')
                    if not opcao_desejada:
                        print(f'{cnpj_cliente_arquivo}: Não tem o fornecedor')
                        with io.open('nao_tem_fornecedor.txt', 'a', encoding='utf-8') as file:
                            file.write(f'{cnpj_cliente_arquivo}\n')
                        continue
                    else:
                        try:
                            select_handle.select_option(value='6453')
                            time.sleep(0.5)
                            inserir_infos(site, cliente)
                            continue
                        except Exception as E:
                            with io.open('erro_no_cliente.txt', 'a', encoding='utf-8') as file:
                                file.write(f'{cnpj_cliente_arquivo}\n')
                            continue
                except Exception as E:
                    print(E)
            return site


def inserir_infos(site, cliente_do_for):
    #input('Selecione o fornecedor e o representante e pressione o enter...')
    #validacao = input('Inserir CNPj em um campo especifico (Deixe vazio se não) ?: ')
    validacao = ''

    if not validacao:
        #linha_validacao = 1  # Valor referencia
        cnpj_cliente_validacao = ''
        lista_cnpjs = []
        while True:
            qtd_linhas = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div'
                                      '/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table'
                                      '/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div[2]/table[2]/tbody'
                                      f'/tr[1]/td/table/tbody/tr').count()

            for linha in range(1, qtd_linhas + 1):
                time.sleep(0.5)

                cnpj_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div'
                                            '/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table'
                                            '/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div[2]/table[2]/tbody'
                                            f'/tr[1]/td/table/tbody/tr[{linha}]/td[2]/span').text_content()
                site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                          '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                          f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{linha}]/td[3]'
                          f'/input', cnpj_cliente)
                site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                          '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                          f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{linha}]/td[4]'
                          f'/input', cnpj_cliente)
                site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                          '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                          f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{linha}]/td[5]'
                          '/input', cnpj_cliente)
                if not cnpj_cliente in lista_cnpjs:
                    lista_cnpjs.append(cnpj_cliente)
            #linha_validacao = linha
            cnpj_cliente_validacao = cnpj_cliente

            try:
                Validar_botao_de_paginar = \
                    site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td'
                             '/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]'
                             '/div[2]/table[2]/tbody/tr[1]/td/table/tfoot/tr/td/div/table/tbody/tr/td[8]').is_visible()
                if Validar_botao_de_paginar:
                    site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td'
                                 '/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]'
                                 '/div[2]/table[2]/tbody/tr[1]/td/table/tfoot/tr/td/div/table/tbody/tr/td[8]').click()
            except Exception as E:
                break
            time.sleep(1)

            cnpj_validacao_se_ja_foi_preenchido = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                      '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                      f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td[5]'
                      '/input').input_value()
            if cnpj_validacao_se_ja_foi_preenchido in lista_cnpjs:
                break
        # input('Clique em salvar as condicoes.')
        element = site.query_selector('input[type="button"][value="Salvar"]')
        element.click()
        time.sleep(0.5)
        # print('Finalizando a automacao :)')
        with io.open('condicoes_salvas.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cliente_do_for}\n')
            print(f"{cliente_do_for}: OK")
        return

    else:
        #  cnpj_aonde = input('Em que campo colocar o cnpj do cliente:\n1 - Codigo\n2 - Usuario\n3 - Senha\n: ')
        cnpj_aonde = ''
        while True:
            for cliente in range(1, 11):  # de 1 a 10
                qtd_linhas = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div'
                                          '/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table'
                                          '/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div[2]/table[2]/tbody'
                                          f'/tr[1]/td/table/tbody/tr').count()
                cnpj_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div'
                                            '/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table'
                                            '/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div[2]/table[2]/tbody'
                                            f'/tr[1]/td/table/tbody/tr[{cliente}]/td[2]/span').text_content()
                if cnpj_aonde == '1':
                    site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                              '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                              f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{cliente}]/td[3]'
                              f'/input', cnpj_cliente)
                if cnpj_aonde == '2':
                    site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                              '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                              f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{cliente}]/td[4]'
                              f'/input', cnpj_cliente)
                if cnpj_aonde == '3':
                    site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                              '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                              f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{cliente}]/td[5]'
                              '/input', cnpj_cliente)

                if qtd_linhas != 10 and qtd_linhas == cliente:
                    input('Clique em salvar as condicoes.')
                    print('Finalizando a automacao :)')
                    return

            site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                         '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/'
                         'tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tfoot/tr/td/div/table/tbody'
                         '/tr/td[15]').click()
            time.sleep(1)


def rodar(site):
    autenticar(site)
    entrar_na_tela_cond(site)
    # try:
    #     inserir_infos(site)
    # except Exception as E:
    #     print(f'Deu problema no processo de inserir informações, reinicie o processo.\n{E}')


with sync_playwright() as p:
    while True:
        try:
            navegador = p.firefox.launch(headless=False)
            site = navegador.new_page()
            rodar(site)
            site.close()
        except Exception as E:
            site.close()
            navegador.close()
            print('Deu um problema, refazendo o processo')
            navegador = p.firefox.launch(headless=False)
            site = navegador.new_page()
            rodar(site)