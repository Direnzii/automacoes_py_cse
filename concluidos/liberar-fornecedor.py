from os import getenv
from playwright.sync_api import sync_playwright
import time

class liberarForn():

    def abrir_arquivo(self, arquivo):
        with open(arquivo) as file:
            arquivo = file.read().replace(",", ' ').split()
        return arquivo

    def autenticar(self):
        time.sleep(0.5)
        usuario = getenv(key='USUARIO_OFICIAL')
        senha = getenv(key='SENHA_OFICIAL')
        site.fill('xpath=//*[@id="frmLogin:username"]', usuario)
        site.fill('xpath=//*[@id="frmLogin:password"]', senha)
        site.locator('xpath=//*[@id="frmLogin:loginButton"]').click()
        time.sleep(0.2)

    def liberar_fornecedor(self):
        self.autenticar()
        for cliente in arquivo:
            cliente = cliente.replace("'", "")
            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]/a/img').click() ######BREAK
            time.sleep(1)
            site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/div/div[2]/table/tbody/tr[2]/td[2]/input'
                      , cliente)
            time.sleep(0.5)
            site.locator('xpath=//*[@id="pesquisarUsuarios:btnPesquisar"]').click() #clicar em pesquisar
            time.sleep(1.5)
            try:
                usuario_visivel = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody'
                                               '/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table'
                                               '/tbody/tr[3]/td/div/div[2]/table/tbody/tr/td[1]/a/img').is_visible() #ver se é possivel ver o usuario
                if usuario_visivel == False:
                    i = 0
                    while i <= 5:
                        usuario_encontrado = site.locator('xpath=//*[@id="inputHiddenMessage"]').text_content()
                        time.sleep(0.3)
                        i += 1
                        if usuario_encontrado == 'Nenhum usuário foi encontrado.':
                            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[2]').click() #não localizou o usuario, clicar na aba clientes
                            time.sleep(1.5)
                            site.fill('xpath=//*[@id="pesquisarClientes:cnpj"]', cliente) #inserir o cnpj do cliente na caixa de busca
                            site.locator('xpath=//*[@id="pesquisarClientes:mostrarFiliais"]').click() #checar a box "mostrar filiais"
                            site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()# clicar em pesquisar"
                            time.sleep(1.5)
                            site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                         '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td'
                                         '/div/div[2]/div/div/table/tbody/tr/td[4]/input').click() #clicar em editar
                            time.sleep(1.5)
                            matriz = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div'
                                                  '/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table'
                                                  '/tbody/tr[2]/td/table/tbody/tr/td/div/div[2]/table/tbody/tr[2]'
                                                  '/td[2]/input').input_value() #pegar o cnpj da matriz
                            cliente = matriz
                            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]').click() #clicar na aba inicio
                            time.sleep(1)
                            site.fill(
                                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/div/div[2]/table/tbody/tr[2]/td[2]/input'
                                , cliente)
                            site.locator('xpath=//*[@id="pesquisarUsuarios:btnPesquisar"]').click()  # clicar em pesquisar
                            time.sleep(1.5)
                            i = 6 #forçar a saida do while

                time.sleep(1.5)
                site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table/tbody/tr[3]' ######BREAK
                         '/td/div/div[2]/table/tbody/tr[1]/td[6]/a').click() #clica em editar
                site.locator(
                    'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]'
                    '/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[6]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]').click() #clica na aba filial para validar
                time.sleep(1.5)
                site.locator(
                    'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]'
                    '/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[8]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]').click() #clica na aba de fornecedores
                time.sleep(1.5)
                fornecedor = '08241229000200 - MILFARMA - SP'
                representante_rm = '39926 - On-line - cotefacil@milfarma.com.br'
                representante = '101385 - REPRESENTANTE COMERCIAL - no-reply@cotefacil.com'
                remover = True # true se for remover um representante antes, false se nao

                site.fill(
                    'xpath=//*[@id="administrarCliente:fornecedor"]'
                    , fornecedor)
                site.fill(
                    'xpath=//*[@id="administrarCliente:sggRepresentante"]'
                    , representante)
                print(f"Representante liberado para o cliente: {cliente}") ######BREAK
                site.locator('#administrarCliente\:j_id277').click()

                if remover == True:
                    site.fill(
                        'xpath=//*[@id="administrarCliente:fornecedor"]'
                        , fornecedor)
                    site.fill(
                        'xpath=//*[@id="administrarCliente:sggRepresentante"]'
                        , representante_rm)
                    site.locator('xpath=//*[@id="administrarCliente:j_id272"]').click() #remover representante
                    time.sleep(0.4)
                    mensagem = ''
                    erro = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody'
                                        '/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/span/div'
                                        '/div/table/tbody/tr/td/table/tbody/tr/td[1]/img').is_visible() #ver se deu erro
                    if erro == True:
                        print(f'Erro para o cliente: {cliente}')

                    print(f"{representante_rm}{mensagem} removido, cliente: {cliente}")  ######BREAK
                    site.locator('xpath=//*[@id="j_id701:j_id708"]').click()  # remover sim
                    time.sleep(1.5)


            except: ######BREAK
                print(f"Erro para o cliente: {cliente}") ######BREAK
                continue

liberar_forn = liberarForn()
with sync_playwright() as p:
    ##### VARIAVEIS DO PLAYWRIGHT #####
    navegador = p.firefox.launch(
        headless=False)  # por padrão esse modo é headless = True (não mostra o navegador abrindo)
    ###################################
    site = navegador.new_page()
    site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')
    arquivo = 'mil.txt'
    arquivo = liberar_forn.abrir_arquivo(arquivo)

    liberar_forn.liberar_fornecedor()