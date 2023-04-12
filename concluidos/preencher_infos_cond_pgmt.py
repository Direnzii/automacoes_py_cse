from os import getenv
from playwright.sync_api import sync_playwright
import time


def autenticar(site):
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


def entrar_na_tela_cond():
    manualmente = input('Deseja inserir as informações e ir até a aba Fornecedores, manualmente ? (S) (N): ')
    site = navegador.new_page()
    # cliente = input('Insira o cnpj do cliente: ')
    cliente = '10834344000150'
    if manualmente == 'S' or manualmente == 's':
        site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')
        autenticar(site)
        input('Processo travado, insira as informações até e entra na aba FORNECEDORES, depois clique em Enter...')
    else:
        site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')
        autenticar(site)
        site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table'
                  '/tbody/tr[1]/td/div/div[2]/table/tbody/tr[2]/td[2]/input', cliente)
        time.sleep(1.5)
        site.locator('xpath=//*[@id="pesquisarUsuarios:btnPesquisar"]').click()
        time.sleep(1.5)

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
    return site


def inserir_infos(site):
    input('Selecione o fornecedor e o representante e pressione o enter...')
    validacao = input('Inserir CNPj em um campo especifico (Deixe vazio se não) ?: ')

    if not validacao:
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
                site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                          '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                          f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{cliente}]/td[3]'
                          f'/input', cnpj_cliente)
                site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                          '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                          f'/tr/td/div[2]/div[2]/table[2]/tbody/tr[1]/td/table/tbody/tr[{cliente}]/td[4]'
                          f'/input', cnpj_cliente)
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
    else:
        cnpj_aonde = input('Em que campo colocar o cnpj do cliente:\n1 - Codigo\n2 - Usuario\n3 - Senha\n: ')
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


def rodar():
    site = entrar_na_tela_cond()
    try:
        inserir_infos(site)
    except:
        print('Deu problema no processo de inserir informações, reinicie o processo.')


with sync_playwright() as p:
    navegador = p.firefox.launch(headless=False)
    rodar()